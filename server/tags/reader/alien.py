from threading import Timer
import serial
from datetime import date, datetime
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from ..models import Entry, Tag


# global state
antenna_tags = ["Tag:3034 0BC9 E41C 3DC2 017A 6403", "Tag:1501 5010 0000 0000 0257 6463"]
tags = {} # history
is_running = False


def handle_detected_tag(tag_id: str, antenna, detected_at):
    # print(tag_id, antenna)
    try:
        tag = Tag.objects.get(tag_name=tag_id) 
        if not tag.is_leaving and not tag.is_returning:
            print(f"{detected_at}: {tag_id} is detected on {antenna} but it is not associated with any movement")
            return None  
        try:
            entry = Entry.objects.get(tag=tag, returned_at=None)
            if tag.is_leaving:
                # update tag info
                tag.has_left = True
                tag.last_time_left = detected_at
                tag.recent_user = entry.user
                # update entry
                entry.antenna = antenna
                entry.left_at = detected_at
                print(f"{detected_at}: {tag_id} has left using {antenna}.")
            elif tag.is_returning:
                # update tag 
                tag.has_left = False
                tag.is_taken = False
                # entry
                entry.returned_at = detected_at
                print(f"{detected_at}:{tag_id} has returned using {antenna}.")
            
            # update the database
            tag.save()
            entry.save()
                
        except Exception as e:
            print(e)
            raise e
                       
    except ObjectDoesNotExist:
        print(f"{tag_id} is not recognized")
        
    except Exception as e:
        raise e
    
        
        
def set_removal_time_from_history(tag_id, minutes=2):
    seconds = minutes * 60
    def remove_tag():
        del tags[tag_id]
    t = Timer(seconds, remove_tag)
    t.start()


def is_tag(text: str):
    if not text.startswith("b'Tag") or not text.__contains__('Ant:'):
        return False
    return True

def time_passed():
    pass


def parse_line(text: str):
    text_list = text.split(',')
    if len(text_list) < 4:
        return None
    id = text_list[0].replace("b'", '')
    last_seen = text_list[2]
    count = text_list[3]
    return id, last_seen, count

def read_tags():
    print('Waiting for tags....')
    cmd = "t" + '\r\n'
    ser = serial.Serial("COM5", 115200)
    while True:
        ser.write(cmd.encode())
        line = ser.readline()
        # print("Undecoded: ", line)
        line = line.strip().decode("utf-8")
        # print("Decoded: ", line)
        if not line or line.startswith("#") or line.startswith("\x00") or line.lower() == "(no tags)":
            continue
        try:
            tag_info = line.split(',')
            tag_id, antenna = tag_info[0], tag_info[4]
            antenna = antenna.strip()
            tag_id = tag_id.strip()
            # check it an antenna itself
            if tag_id in antenna_tags:
                continue
            if not tag_id in tags:
                detected_at = datetime.now(tz=timezone.utc)
                tags[tag_id] = {
                    "antenna": antenna,
                    "detected_at": detected_at
                }
                # call the function to handle the detected tag 
                handle_detected_tag(tag_id, antenna, detected_at)
                # remove the tag from detected tags after specified minutes
                set_removal_time_from_history(tag_id)  
        except IndexError:
            continue
        
        # except KeyboardInterrupt:
        #     ser.close()

def setTimeOut(seconds, callback):
    s = Timer(seconds, callback)
    s.start()


     
# if __name__ == '__main__':
#     read_tags()
#     pass