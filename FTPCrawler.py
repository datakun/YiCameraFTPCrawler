import ftplib

import datetime

import os

import config


def save_from_ftp(ftp_url, ftp_port, username, password, server_directory, local_directory):
    # 23일마다 파일을 정리해야 함. 하루에 대략 6.5GB, 라즈베리파이 가용 용량은 대략 150GB, 6.5 / 150 = 23.xxx
    ftp = ftplib.FTP()
    ftp.connect(ftp_url, ftp_port)
    ftp.login(username, password)
    ftp.cwd(server_directory)

    filename_list = ftp.nlst()

    for file in filename_list:
        if os.path.exists(local_directory + file) is True:
            stat_info = os.stat(local_directory + file)
            if stat_info.st_size > 1024:
                print('"' + file + '" is exists.')

                continue

        fd = open(local_directory + file, 'wb')

        try:
            ftp.retrbinary("RETR " + file, fd.write)
        except ftplib.Error as e:
            print(e)

        fd.close()

        print('"' + file + '" is downloaded.')


if __name__ == "__main__":
    target_datetime = datetime.datetime.now() + datetime.timedelta(hours=-1)
    target_time = target_datetime.strftime('%YY%mM%dD%HH')

    save_from_ftp(config.FTP_URL, config.FTP_PORT, config.USERNAME, config.PASSWORD, '/tmp/hd1/record/' + target_time + '/', './')
