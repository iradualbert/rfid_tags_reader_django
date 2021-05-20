from threading import Timer
import time
import serial

ser = serial.Serial("COM5", 115200)

cmd = "t" + '\r\n'

product_tags = {'Tag:3500 0000 00A0 10B4 DA50 078A', 'Tag:3500 0000 00A0 17BE C23F 4E9E'}
antenna_tags = ["Tag:3034 0BC9 E41C 3DC2 017A 6403", "Tag:1501 5010 0000 0000 0257 6463"]
user_tags = {'Tag:3500 0000 00FF 882E B4C3 BF6B'}
history = {}


def set_removal_time_from_history(tag_id, minutes=0.1):
    seconds = minutes * 60
    def remove_tag():
        # print('I am the delete function')
        del history[tag_id]
    t = Timer(seconds, remove_tag)
    t.start()
        
def parse_lines(lines):
    current_product_tags = set()
    current_user_tags = set()
    for line in lines:
        try:
            tag_info = line.split(',')
            tag_id, antenna = tag_info[0], tag_info[4]
            antenna = antenna.strip()
            tag_id = tag_id.strip()
            if tag_id in history:
                continue
            if tag_id in antenna_tags:
                continue
            elif tag_id in user_tags:
                current_user_tags.add(tag_id)
            elif tag_id in product_tags:
                current_product_tags.add(tag_id)
        except IndexError:
            continue
        except Exception as e:
            raise e
    diff_tags = list(product_tags.difference(current_product_tags))
    missing_tags = []
    for tag in diff_tags:
        if not tag in history:
            history[tag] = tag
            missing_tags.append(tag)
            # set_removal_time_from_history(tag)
    return missing_tags

def read_all():
    while True:
        time.sleep(0.2)
        ser.write(cmd.encode())
        waiting = ser.inWaiting()
        buffer_string = ser.read(waiting).strip().decode("utf-8")
        lines = buffer_string.splitlines()
        print(buffer_string)
        if len(lines) == 0:
            continue
        else:
            missing_tags = parse_lines(lines)
            # for tag in missing_tags:
            #     print(tag, "is missing")       

if __name__ == "__main__":
    # scan_tags()
   read_all()
