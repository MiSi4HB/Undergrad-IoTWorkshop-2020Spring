import serial
from tkinter import *
import threading
from datetime import datetime

print('Connecting...')
ser = serial.Serial('COM3', 250000, timeout=1)
if ser.isOpen():
    print('Connected!')

on = True
loop_active = True
data_receive = True

data_save = None
save_flag = 0
test_trial = 1
time_prev = 0
time_now = 0
time=0

#주행,멈춤 변수
acc_tot=0 #가속도total값
state='주행' #주행, 멈춤

#경사로 변수
gyeong=0#경사로상태구분
gtime_1=0#경사로 시간prev
gtime_2=0#경사로 시간cur
gtime=0

#넘어짐 변수
a1=0#넘어짐구분
a2=0#넘어짐구분
fdtime_1=0#넘어짐 시간 prev
fdtime_2=0#넘어짐 시간 cur
fdtime=0

#충돌 변수
a3=0#충돌구분
ctime_p=0#충돌시간 과거
ctime_c=0#충돌시간 현재
ctime_1=0#충돌레이블시간1
ctime_2=0#충돌레이블시간2
ctime=0#현재-과거 시간
choong=0#충돌상태
choongtime=0#충돌레이블시간



#도움요청 변수
t_prev=0#터치시간1
t_cur=0#터치시간2
elapsed_t=0 #터치시간
touch=0 #터치count
x1=0 #터치데이터
helptime_1=0#도움요청시간1
helptime_2=0#도움요청시간2
help=0#도움요청상태
helptime=0#도움요청시간




b_prev=0#끼임시간1
b_cur=0#끼임시간2
b_time=0#끼임레이블시간




a4=0#끼임구분
x2=0#끼임
b=0#끼임
btime_p=0
btime_c=0
btime_t=0



def ser_write():
    global on
    if on:
        ser.write(b'0248')
    else:
        ser.write(b'1359')
    on = not on

class Upd(threading.Thread):

    def __init__(self, tk_root):
        self.root = tk_root
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        global loop_active, save_flag, time, data_save, time_prev, time_nowa, btime_p,btime_c,btime_t, touch, x1,x2, state,num,b, t_prev,t_cur,elapsed_t,helptime_1, a2,a1, helptime_2, help, helptime, gyeong, acc_tot,a3,ctime_c,ctime_p,ctime_1,ctime_2,ctime,choong,choongtime,a4,b_time,b_prev,b_cur,gtime,gtime_1,gtime_2,fdtime,fdtime_1,fdtime_2
        while loop_active:
            if data_receive:
                x = ser.readline()
                x = x.split()
                if len(x) > 7:
                    #이부분에 코드짜기
                    acc_tot=(float(x[2])**2+float(x[3])**2+float(x[4])**2)**0.5
                    date= str(datetime.now().year)+"-"+str(datetime.now().month)+"-"+str(datetime.now().day)
                    datenow.configure(text=date)
                    time=str(datetime.now().hour)+":"+str(datetime.now().minute)+":"+str(datetime.now().second)
                    timenow.configure(text=time)

                    # 멈춤
                    if float(acc_tot) <= 1.02 and float(acc_tot) >= 0.99:
                        state = '멈춤'



                    else:
                        state = '주행'
                    status.configure(text=state)

                    #경사로
                    if gyeong==0:
                        if float(x[3]) >= 0.3:
                            gyeong=1
                            gtime_1=datetime.now()

                    else:
                        gtime_2=datetime.now()
                        gtime=(gtime_2 - gtime_1).total_seconds()
                        if gtime>=1:
                            status_g.configure(text='경사로', fg="red")
                        if float(x[3])<0.2:
                            gyeong=0
                            status_g.configure(text= "평지", fg="gray")

                    #넘어짐
                    if a2 == 0:
                        if (float(x[2])>=0.9 and float(x[2])<=1.08 and float(x[4])>=0.05 and float(x[4])<=0.19) or (float(x[2])>=-1.08 and float(x[2])<=-0.98 and float(x[4])>=0.07 and float(x[4])<=0.16):
                            a2 = 1
                            status_fd.configure(fg="red")
                    else:
                        if (float(x[2])>=0.9 and float(x[2])<=1.08 and float(x[4])>=0.05 and float(x[4])<=0.19) or (float(x[2])>=-1.08 and float(x[2])<=-0.98 and float(x[4])>=0.07 and float(x[4])<=0.16):
                            continue
                        else:
                            a2 = 0
                            status_fd.configure(fg="gray")

                    #충돌시간
                    if choong==1:
                        ctime_2 = datetime.now()
                        choongtime=(ctime_2 - ctime_1).total_seconds()
                        if choongtime >= 2.3:
                            status_c.configure(fg="gray")
                    #충돌
                    if a3==0:
                        if float(acc_tot)>=2.7:
                            a3=1
                            ctime_p=datetime.now()

                    else:
                        if float(acc_tot)<= 2.0:
                            a3=0
                            ctime_c=datetime.now()
                            ctime = (ctime_c - ctime_p).total_seconds()
                            if ctime < 0.2 and ctime > 0:
                                choong=1
                                status_c.configure(fg="red")
                                ctime_1=datetime.now()

                    #도움요청시간
                    if help==1:
                        helptime_2 = datetime.now()
                        helptime=(helptime_2 - helptime_1).total_seconds()
                        if helptime >= 5.0:
                            status_h.configure(fg="gray")

                    # 도움요청
                    if float(x[1])==0:
                        x1=0

                    if x1==0:
                        if float(x[1]) == 1:
                            touch+=1
                            x1=1
                    if touch==1:
                        t_prev= datetime.now()
                    if touch==3:
                        t_cur = datetime.now()
                        elapsed_t = (t_cur - t_prev).total_seconds()
                        if elapsed_t <= 4.0:
                           touch = 0
                           helptime_1= datetime.now()
                           help=1
                           status_h.configure(fg="red")
                        else:
                           touch=0

                   #걸림
                    if b==1:
                        b_cur=datetime.now()
                        b_time=(b_cur - b_prev).total_seconds()
                        if b_time >= 3:
                            status_b.configure(fg='gray')

                    if a4==0:
                        if float(acc_tot)>=1.7:
                            a4=1
                            btime_p=datetime.now()

                    else:
                        if float(acc_tot)<= 1.7:
                            a4=0
                            btime_c=datetime.now()
                            btime_t = (btime_c - btime_p).total_seconds()
                            if btime_t < 0.2:
                                x2+=1
                    if x2 == 1:
                        t_prev = datetime.now()
                    if x2 == 5:
                        t_cur = datetime.now()
                        elapsed_t = (t_cur - t_prev).total_seconds()
                        if elapsed_t <= 13.0:
                            x2 = 0
                            b_prev = datetime.now()
                            status_b.configure(fg="red")
                            b = 1
                            rec_start()
                        else:
                            a4 = 0

                    #걸림 저장
                    if save_flag == 1:
                        time_now = datetime.now() #현재시간
                        elapsed = (time_now - time_prev).total_seconds()
                        data_save.writelines(str(t_prev) + " - "+str(t_cur)+"  걸림상황 ")
                        rec_stop()



        ser.close()
        self.root.quit()
        self.root.update()

def loop_trigger():
    global data_receive
    if data_receive:
        data_receive = False
        ser.write(b's')
        bt2.configure(text="시작")
    elif not data_receive:
        data_receive = True
        ser.write(b'r')
        bt2.configure(text="정지")

def rec_start():
    global data_save, save_flag, test_trial, time_prev
    data_save = open("test" + str(test_trial) + ".txt", "w")
    save_flag = 1
    time_prev = datetime.now()

def rec_stop():
    global data_save, save_flag, test_trial
    data_save.close()
    test_trial += 1
    save_flag = 0

def exitProgram():
    global loop_active
    loop_active = False

win = Tk()
win.title("rotafy")
win.geometry("350x450")
upd = Upd(win)
win.resizable(width= FALSE, height =FALSE)

title=Label(win, text="Rotafy",font=("STCaiyun",40), fg="#45818e")
title.pack(padx=10)
name=Label(win, text="휠체어 안전알리미",font=("나눔고딕"), fg="#ea9999")
name.pack(padx=10)

now=Label(win, text="<휠체어 상태>",font=("나눔고딕",10), fg="black")
now.pack(padx=10, pady=22)


status= Button(win, text = state,width=7, height=2)
status.place(x=102, y=131)
status_g= Button(win, text = "평지", fg="gray",width=7, height=2)
status_g.place(x=182, y=131)
status_h= Button(win, text = "도움요청", fg="gray",width=7, height=2)
status_h.place(x=102, y=191)
status_fd= Button(win, text = "넘어짐", fg="gray",width=7, height=2)
status_fd.place(x=182, y=191)
status_c= Button(win, text = "충돌", fg="gray",width=7, height=2)
status_c.place(x=102, y=251)
status_b= Button(win, text = "걸림", fg="gray",width=7, height=2)
status_b.place(x=182, y=251)

datenow=Label(win, text="-")
datenow.place(x=140, y=315)
timenow=Label(win, text="-")
timenow.place(x=148, y=335)


bt5 = Button(win, text = '종료', command = exitProgram, fg="#45818e")
bt5.pack(side="bottom", fill=X, padx=10, pady=7)
bt2 = Button(win, text='정지', command=loop_trigger, fg="#45818e")###시작-->정지
bt2.pack(side="bottom", fill=X, padx=10, pady=1)

win.mainloop()
