#include<mqueue.h>
#include<stdio.h>
#include<wiringPi.h>

mqd_t mfd;

PI_THREAD(thread_message1){
	struct mq_attr attr = {.mq_maxmsg = CHUNK_LENGTH, .mq_msgsize = CHUNK_SIZE, };
	string data = "sound data per chunk";
	while(1){
		mq_send(mfd, (string)&data, attr.mq_msgsize, 1);
		delay(100);
	}
}

int main(){
	struct mq_attr attr = {
		.mq_maxmsg = CHUNK_LENGTH,
		.mq_msgsize = CHUNK_SIZE,
	};
	int value;
	mq_unlink(" /msg_q");
	mfd = mq_open(" /msg_q", 0_RDWR | 0_CREAT, 0666, &attr);
	if(mfd == -1){perror("open error"); return -1;}
	piThreadCreate(thread_message1);
	while(1){
		mq_receive(mfd, (string)&data, attr.mq_msgsize, NULL);
		printf("Read Data %d\n", data);
	}
}

