import sys
import request_message

def read_file_continue():
    failed_continue_times = 0
    while True:
        line = sys.stdin.readline()
        print(line, end='')
        #Oct  8 09:08:25 raspberrypi sshd[10358]: Failed password for root from 186.42.238.101 port 38352 ssh2
        if 'sshd' in line:
            if 'Failed password' in line:
                failed_continue_times += 1
                if failed_continue_times == 3:
                    if len(line.split()) < 14:
                        user_name = line.split()[8]
                        from_ip = line.split()[10]
                        text = f'{from_ip} が{user_name}の認証失敗したよ'
                        print(text)
                        request_message.send_message(text)
            else:
                failed_continue_times = 0
            if 'Accepted password' in line:
                if len(line.split()) < 14:
                    user_name = line.split()[8]
                    from_ip = line.split()[10]
                    text = f'{user_name}が{from_ip}からログインしたよ'
                    print(text)
                    request_message.send_message(text)
