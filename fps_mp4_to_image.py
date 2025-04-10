#!/usr/bin/python

__author__ = 'wehh'

import traceback

'''
输入最大帧号和最小帧号，输出是对应帧的image
'''
# -*- coding: UTF-8 -*-
import ffmpeg
import numpy
import cv2
import sys
import random
import os
import datetime
import av
import sys

def read_frame_as_jpeg(in_file, out,frame_num,max_frame):
    """
    指定帧数读取任意帧
    """

    # out, err = (
    #     ffmpeg.input(in_file)
    #           .filter('select', 'gte(n,{})'.format(frame_num))
    #           .output('pipe:', vframes=1, format='image2', vcodec='mjpeg')
    #           .run(capture_stdout=True)

    vc = cv2.VideoCapture(in_file) #读入视频文件
    #print(out)

    c=0 #计数 统计对应帧号

    rval=vc.isOpened() #判断视频是否打开 返回True或Flase
    #print(rval,in_file)
    if not os.path.exists(out):
        os.makedirs(out)


    while rval: #循环读取视频帧

        rval, frame = vc.read() #videoCapture.read() 函数，第一个返回值为是否成功获取视频帧，第二个返回值为返回的视频帧：
        #cv2.imwrite(str(c)+ '_' + '.jpg', frame)
        if rval:
            # print("当前帧号：",c)
            if c<int(frame_num)-1:
                c = c + 1
                continue

            if c>int(frame_num)-1 and c< int(max_frame):
                #print(c,rval)
                #print(c)

                if c%1!=0:
                    c = c + 1
                    continue

                try:
                    now_time = datetime.datetime.now()
                    now_time = "".join(list(filter(str.isdigit, str(now_time))))

                    #cv2.imwrite( out+"\\"+str(c)+ '_' + '.jpg', frame) #存储为图像,保存名为 文件夹名_数字（第几个文件）.jpg
                    cv2.imencode('.jpg', frame)[1].tofile(out+"\\" +"frame"+"-"+ str(c)+'.jpg')
                except:
                    traceback.print_exc()
                    break
                #cv2.imshow('frame', frame)
                #cv2.waitKey(1) #waitKey()--这个函数是在一个给定的时间内(单位ms)等待用户按键触发;如果用户没有按下 键,则接续等待(循环)
            elif c>int(max_frame)+1:
                break

            c = c + 1

            #print(rval)
        else:
            break
    vc.release()



def get_video_info(in_file):
    """
    获取视频基本信息
    """
    try:

        probe = ffmpeg.probe(in_file)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        if video_stream is None:
            print('No video stream found', file=sys.stderr)
            sys.exit(1)
        return video_stream
    except ffmpeg.Error as err:
        print(str(err.stderr, encoding='utf8'))
        sys.exit(1)

def get_source_info_opencv(source_name):
    return_value = 0
    try:
        print(source_name)
        cap = cv2.VideoCapture(source_name)
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH )
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        fps = cap.get(cv2.CAP_PROP_FPS)
        num_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        print("width:{} \nheight:{} \nfps:{} \nnum_frames:{}".format(width, height, fps, int(num_frames)))
    except (OSError, TypeError, ValueError, KeyError, SyntaxError) as e:
        print("init_source:{} error. {}\n".format(source_name, str(e)))
        return_value = -1
    return return_value





def h265ToJpg_demo(inputFileName):

    container = av.open(inputFileName)


    print("container:", container)
    print("container.streams:", container.streams)
    print("container.format:", container.format)
    save_dir=os.path.dirname(inputFileName)
    for frame in container.decode(video=0):
        print("process frame: %04d (width: %d, height: %d)" % (frame.index, frame.width, frame.height))
        frame.to_image().save(save_dir+"\\frame-%04d.jpg" % frame.index)


if __name__ == '__main__':
    file_path = u"E:\\work\\相关数据\\标定数据\\1\\"
    out=u"E:\\work\\相关数据\\标定数据\\1\\frame"
    #inputFileName = r"D:\temp1\05-FusionFlowchongqing\data-feicheng\v_37.101.158.79_1698895264537.ts"

    #out=u"V:\\1-测试数据\9-合肥园区采集工具数据\\7.2022-01-12延时测试\第四组东向西高速\\vision\\image"

    #h265ToJpg_demo(inputFileName)
    #获取视频信息
    pathlist = os.listdir(file_path)
    for each_path in pathlist:
        if 'ts' not in each_path:
            continue
        file_path=os.path.join(os.path.dirname(file_path),os.path.basename(each_path))
        get_source_info_opencv(file_path)

        read_frame_as_jpeg(file_path, out, 0, 1627)
    '''
    ffmpeg方式获取视频信息，暂时获取不到总帧数，有时间再排查原因
    # video_info = get_video_info(file_path)
    # print(video_info)
    # total_frames = int(video_info['nb_frames'])
    # print('总帧数：' + str(total_frames))
    # random_frame = random.randint(1, total_frames)
    # print('随机帧：' + str(random_frame))
    '''
    #获取第0~100帧图片，并保存到out目录





    #cv2.imshow('frame', image)
    #cv2.waitKey()


