from threading import Timer
import time
import serial
from ..models import Entry, Tag, Profile, Antenna


class TagReader(object):
    user_tags = {'Tag:3500 0000 00FF 882E B4C3 BF6B'}
    product_tags = {'Tag:3500 0000 00A0 10B4 DA50 078A', 'Tag:3500 0000 00A0 17BE C23F 4E9E'}
    antenna_tags = ["Tag:3034 0BC9 E41C 3DC2 017A 6403", "Tag:1501 5010 0000 0000 0257 6463"]
    bag_antenna_names = set()

    def __init__(self):
        self.history = {}
        self.returned_history = {}
        self.missing_tags = []
        self.current_tags = set()
    
    def should_ignore(self, tag):
        if tag in self.history or tag in self.antenna_tags:
            return True
        return False

    def add_to_history(self, tag, **kwargs):
        self.history[tag] = tag
        self.set_removal_from_history(tag, **kwargs)

    def _remove_from_history(self, tag):
        del self.history[tag]

    def set_removal_from_history(self, tag, minutes=1):
        seconds = minutes * 60
        t = Timer(seconds, self._remove_from_history, args=[tag,])
        t.start()


    @classmethod
    def update_data_from_db(cls):
        cls.user_tags = Profile.get_all()
        cls.tags = Tag.get_all()
        cls.antenna_tags = Antenna.get_all()
        cls.bag_antenna_names = Antenna.get_bag_antenna_names()
        

    def start(self):
        self.update_data_from_db()
        self.read_all()


    def read_all(self):
        self.ser = serial.Serial("COM5", 115200)
        while True:
            time.sleep(0.5)
            cmd = "t" + '\r\n'
            self.ser.write(cmd.encode())
            buffer_string = self.ser.read(self.ser.inWaiting()).strip().decode("utf-8")
            lines = buffer_string.splitlines()
            if len(lines) == 0:
                continue
            else:
                self.handle_lines(lines)


    def handle_lines(self, lines):
        current_tags = set()
        current_users = set()
        # print("Lines", lines)
        for line in lines:
            try:
                tag_info = line.split(',')
                tag_id, antenna = tag_info[0], tag_info[4]
                antenna_name = antenna.strip()
                tag_id = tag_id.strip()
                # current_tags.add(tag_id)
                # print(tag_id)
                if self.should_ignore(tag_id):
                    continue
                # update current tags before handling the detected user
                elif tag_id in self.tags:
                    # make sure that the tag is detected by the bag antenna
                    # if antenna_name in self.bag_antenna_names:
                    current_tags.add(tag_id)
                elif tag_id in self.user_tags:
                    current_users.add(f"{tag_id},{antenna_name}")
            except IndexError:
                continue
            except Exception as e:
                raise e
        self.current_tags = current_tags
        # print(current_tags)
        # update the returned tags
        self.handle_returned_tags()
        for user in current_users:
            tag_id, antenna_name = user.split(",")
            self.handle_user(tag_id, antenna_name)


    def handle_returned_tags(self):
        returned_tags = Tag.objects.filter(is_taken=True, tag_id__in=self.current_tags)
        for tag in returned_tags:
            tag.is_taken = False
            print(f"{tag.tag_id} is returned!")
            tag.save()

    #
    def handle_user(self, user_tag_id, antenna_name):
        self.add_to_history(user_tag_id, minutes=0.05)
        person = self.user_tags[user_tag_id]
        antenna = Antenna.objects.get(name=antenna_name)
        bag = antenna.bag
        # check whether the antenna is a door or a bag antenna
        if bag:
            if not bag.is_closed  and bag.current_user != person:
                print(f"{bag} not available now.")
            elif bag.is_closed:
                bag.open(person=person)
                print(f"{person} has opened the {bag} bag.")
            else:
                bag.close(person=person)
                taken_tags = self.get_taken_tags(bag)
                taken_ids = ', '.join([x.name for x in taken_tags]) 
                entry = Entry(user=person, bag=bag)
                entry.save()
                for tag in taken_tags:
                    tag.is_taken = True
                    entry.taken_tags.add(tag)
                    tag.save()
                print(f"{person} has closed the  bag.")
                if taken_tags:
                    print(f"{person} took {taken_ids}")

        # Else if the user is detected at the door
        # TO DO
        else:
            pass


    # get taken bags
    def get_taken_tags(self, bag):
        bag_tags = Tag.objects.filter(bag=bag)
        not_taken_tags = bag_tags.filter(is_taken=False)
        # missing_tags = bag_tags.exclude(tag_id__in=self.current_tags)
        taken_tags = not_taken_tags.exclude(tag_id__in=self.current_tags)
        # print("All Missing: ", missing_tags)
        # print("Taken:", taken_tags)
        # print("Available", self.current_tags)
        return taken_tags


