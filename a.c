 #include<reg52.h>
 #include<instrins.h>
 #include<math.h>
 #include<stdio.h>
 #define LCD_DB P0
 sbit LCD_RS=P1^0;
 sbit LCD_RW=P1^1;
 sbit LCD_E=P1^2;
 #define uchar unsigned char
 #define uint unsigned int
 typedef unsigned long U32;
 typedef signed long S32;
 typedef float F32;
 void LCD_init(void);
 void LCD_write_command(uchar command);
 void LCD_write_data(ucahr dat);
 void LCD_disp_char(uchar x,uchar y,uchar dat);
 void LCD_disp_str(uchar x,uchar y,uchar *str);
 void delay_n10us(uint n);
 void LCD_init(void){
 	delay_n10us(10);
	LCD_write_command(0x38);
	delay_n10us(10);
	LCD_write_command(0x0c);
	delay_n10us(10);
	LCD_write_command(0x06);
	delay_n10us(10);
	LCD_write_command(0x01);
	delay_n10us(100);
 }
 void LCD_write_command(uchar dat){
 	delay_n10us(10);
	LCD_RS=0;
	LCD_RW=0;
	LCD_E=1;
	LCD_DB=dat;
	delay_n10us(10);
	LCD_E=0;
	delay_n10us(10);
 }
 void LCD_write_data(uchar dat){
 	delay_n10us(10);
	LCD_RS=1;
	LCD_RW=0;
	LCD_E=1;
	LCD_DB=dat;
	delay_n10us(10);
	LCD_E=0;
	delay_n10us(10);
 }
 void LCD_disp_char(uchar x,uchar y,uchar dat){
 	uchar address;
	if(y==1)
		address=0x80+x;
	else
		address=0xc0+x;
	LCD_write_command(address);
	LCD_write_data(dat);
 }
 void LCD_disp_str(uchar x,uchar y,uchar *str){
 	uchar address;
	if(y==1)
		address=0x80+x;
	else
		address=0xc0+x;
	LCD_write_command(address);
	while(*str!='\0'){
		LCD_write_data(*str);
		str++;
	}
 }
 void delay_n10us(uint n){
 	uint i;
	for(i=n;i>0;i--){
		_nop_();_nop_();_nop_();_nop_();_nop_();_nop_();		 //¿ØÖÆÑÓÊ±
	}
 }
 bit set_temp_up=0;
 bit set_temp_down=0;
 bit set_humidity_up=0;
 bit set_humidity_down=0;
 sbit SCK = P3^2;
 sbit DATA = P3^3;
 sbit D1=P3^4;
 sbit D2=P3^5;
 sbit D3=P3^6;
 sbit D4=P3^7;
 sbit key_set=P1^3;
 sbit key_up=P1^4;
 sbit key_down=P1^5;
 uchar selectnum=0,downnum=0,checknum;
 uchar value_shi,value_ge,downnum_shi,downnum_ge;
 uchar shidu_shi,shidu_ge,wendu_shi,wendu_ge;
 sbit PWMZ = P2^0;
 sbit PWMF = P2^1;
 sbit PWMZ2 = P2^3;
 sbit PWMF2 = P2^4;
 sbit Alarm = P2^5;
 bit temp_alarm_flag=1;
 bit rh_alarm_flag=1;
 unsigned char CYCLE;
 unsigned char PWM_ON;
 uchar flag;
 unsigned char CYCLE2;
 unsigned char PWM_ON2;
 uchar flag2;
 uchar temp_uplimit,temp_lowlimit,humidity_uplimit,humidity_lowlimit;
 unsigned int Alarm_temp_up=260;
 Alarm_temp_low=240;
 Alarm_humidity_up=700;
 Alarm_humidity_low=500;
 unsigned int wendu,shidu;
 typedef union{
 	unsigned int i;
	flaot f;
 }value;
 enum{TEMP,HUMI};
 #define noACK 0
 #define ACK 1
 #define STATUS_REG_W 0x86
 #define STATUS_REG_R 0x07
 #define MEASURE_TEMP 0x03
 #define MEASURE_HUMI 0x05
 #define RESET 0x1e
 void s_transstart(void);
 void s_connectionreset(void);
 char s_write_byte(unsigned char value);
 char s_read_byte(unsigned char ack);
 char s_measure(unsigned char *p_value,unsigned char *p_checksum,unsigned char mode);
 void calc_dht90(float *p_humidity,float *p_temperature);
 void s_transstart(void){
 	DATA=1;SCK=0;
	_nop_();
	SCK=1;
	_nop_();
	DATA=0;
	_nop_();
	SCK=0;
	_nop_();_nop_();_nop_();
	SCK=1;
	_nop_();
	DATA=1;
	_nop_();
	SCK=0;
 }
 void s_connectionreset(void){
 	unsigned char i;
	DATA=1;
	SCK=0;
	for(i=0;i<9;i++){
		SCK=1;
		SCK=0;
	}
	s_transstart();
 }
 void delay1ms(uint z){
 	uint x,y;
	for(x=z;x>0;x--)
	for(y=110;y>0;y--);
 }
 char s_write_byte(unsigned char value){
 	unsigned char i,error=0;
	for(i=0x80;i>0;i/=2){
		if(i&value) DATA = 1;
		else DATA =0;
		SCK=1;
		_nop_();_nop_();_nop_();
		SCK=0;
	}
	DATA=1;
	SCK=1;
	error=DATA;
	_nop_();_nop_();_nop_();
	SCK=0;
	DATA=1;
	return error;
 }
 char s_read_byte(unsigned char ack){
 	unsigned char i,val=0;
	DATA=1;
	for(i=0x80;i>0;i/=2){
		SCK=1;
		if(DATA) val=(val|i);
		_nop_();_nop_();_nop_();
		SCK=0;
	}
	if(ack==1)DATA=0;
	else DATA=1;
    _nop_();_nop_();_nop_();
	SCK=1;
	_nop_();_nop_();_nop_();
	SCK=0;
	_nop_();_nop_();_nop_();
	DATA=1;
	return val;
 }
 char s_measure(unsigned char *p_value,unsigned char *p_checksum,unsigned char mode){
 	unsigned error=0;
	unsigned int i;
	s_transstart();
	switch(mode){
		case TEMP:error+=s_write_byte(MEASUPE_TEMP);break;
		case TEMP:error+=s_write_byte(MEASUPE_HUMI);break;
		default:break;
	}
	for(i=0;i<65535;i++) if(DATA==0) break;
	if(DATA) error+=1;
	*(p_value)=s_read_byte(ACK);
	*(p_value+1)=s_read_byte(ACK);
	*p_checksum=s_read_byte(noACK);
	return error;
 }
 void calc_dht90(float *p_humidity,float *p_temperature){
 	const float C1=-4.0;
	const float C2=+0.0405;
	const float C3=-0.0000028;
	const float T1=+0.01;
	const float T2=+0.00008;
	float rh=*p_humidity;
	float t=*p_temperature;
	float rh_lin;
	float rh_true;
	float t_C;
	t_C=t*0.01-40;
	rh_lin=C3*rh*rh+C2*rh+C1;
	rh_true=(t_C-25)*(T1+T2*rh)+rh_lin;
	if(rh_true>100)rh_true=100;
	if(rh_true<0.1)rh_true=0.1;
	*p_temperature=t_C;
	*p_humidity=rh_true;
 }
 void Key_function_scan(){
 	if(key_set==0){
		delay1ms(10);
		if(key_set==0){
			TR0=0;
			TR1=0;
			LCD_disp_str(0,1,"      ");
			LCD_disp_str(0,2,"      ");
			selectnum++;
			if(selectnum==1){
				set_temp_up=1;
				set_temp_down=0;
				set_humidity_up=0;
				set_humidity_down=0;
				LCD_disp_str(0,1,"Set_Temp_Height");
				LCD_disp_char(5,2,(Alarm_temp_up%1000)/100+'0');
				LCD_disp_char(6,2,(Alarm_temp_up%100/10+'0'));
				LCD_disp_char(7,2,'.');
				LCD_disp_char(8,2,(Alarm_temp_up%10)+'0'); 
			}
			if(selectnum==2){
				set_temp_down=1;
				set_temp_up=0;
				set_humidity_up=0;
				set_humidity_down=0;
				LCD_disp_str(0,1,"Set_Temp_Low");
				LCD_disp_char(5,2,(Alarm_temp_low%1000)/100+'0');
				LCD_disp_char(6,2,(Alarm_temp_low%100/10+'0'));
				LCD_disp_char(7,2,'.');
				LCD_disp_char(8,2,(Alarm_temp_low%10)+'0'); 
			}
			if(selectnum==3){
				set_humidity_up=1;
				set_humidity_down=0;
				set_temp_down=0;
				set_temp_up=0;
				LCD_disp_str(0,1,"Set_Hum_Hight");
				LCD_disp_char(5,2,(Alarm_humidity_up%1000)/100+'0');
				LCD_disp_char(6,2,(Alarm_humidity_up%100/10+'0'));
				LCD_disp_char(7,2,'.');
				LCD_disp_char(8,2,(Alarm_humidity_up%10)+'0'); 
			}
			if(selectnum==4){
				set_humidity_down=1;
				set_humidity_up=0;
				set_temp_down=0;
				set_temp_up=0;
				LCD_disp_str(0,1,"Set_Hum_Low");
				LCD_disp_char(5,2,(Alarm_humidity_low%1000)/100+'0');
				LCD_disp_char(6,2,(Alarm_humidity_low%100/10+'0'));
				LCD_disp_char(7,2,'.');
				LCD_disp_char(8,2,(Alarm_humidity_low%10)+'0'); 
			}
			if(selectnum==5){
				LCD_disp_str(0,1,"       ");
				LCD_disp_str(0,2,"       ");
				selectnum=0;
				set_humidity_up=0;
				set_humidity_down=0;
				set_temp_down=0;
				set_temp_up=0;
				LCD_disp_str(0,1,"Temper:     ");
				LCD_disp_str(0,2,"Humidity:     ");
			}
			while(!key_set);
		}
	}
	if(key_up==0){
		delay1ms(10);
		if(key_up==0){
			if(set_temp_up==1){
				Alarm_temp_up++;
				if(Alarm_temp_up==999)Alarm_temp_up=0;
				LCD_disp_char(5,2,(Alarm_temp_up%1000)/100+'0');
				LCD_disp_char(6,2,(Alarm_temp_up%100)/10+'0');
				LCD_disp_char(7,2,'.');
				LCD_disp_char(8,2,(Alarm_temp_up%10)+'0');
			}
			if(set_humidity_up==1){
				Alarm_humidity_up++;
				if(Alarm_humidity_up==999)Alarm_humidity_up=0;
				LCD_disp_char(5,2,(Alarm_humidity_up%1000)/100+'0');
				LCD_disp_char(6,2,(Alarm_humidity_up%100)/10+'0');
				LCD_disp_char(7,2,'.');
				LCD_disp_char(8,2,(Alarm_humidity_up%10)+'0');
			}
			if(set_temp_down==1){
				Alarm_temp_low++;
				if(Alarm_temp_low==999)Alarm_temp_low=0;
				LCD_disp_char(5,2,(Alarm_temp_low%1000)/100+'0');
				LCD_disp_char(6,2,(Alarm_temp_low%100)/10+'0');
				LCD_disp_char(7,2,'.');
				LCD_disp_char(8,2,(Alarm_temp_low%10)+'0');
			}
			if(set_humidity_down==1){
				Alarm_humidity_low++;
				if(Alarm_humidity_low==999)Alarm_humidity_low=0;
				LCD_disp_char(5,2,(Alarm_humidity_low%1000)/100+'0');
				LCD_disp_char(6,2,(Alarm_humidity_low%100)/10+'0');
				LCD_disp_char(7,2,'.');
				LCD_disp_char(8,2,(Alarm_humidity_low%10)+'0');
			}
			while(!key_up);
		}
	}
	if(key_down==0){
		delay1ms(10);
		if(key_down==0){
			if(set_temp_down==1){
				Alarm_temp_low--;
				if(Alarm_temp_low==0)Alarm_temp_low=999;
				LCD_disp_char(5,2,(Alarm_temp_low%1000)/100+'0');
				LCD_disp_char(6,2,(Alarm_temp_low%100)/10+'0');
				LCD_disp_char(7,2,'.');
				LCD_disp_char(8,2,(Alarm_temp_low%10)+'0');
			}
			if(set_humidity_down==1){
				Alarm_humidity_low--;
				if(Alarm_humidity_low==0)Alarm_humidity_low=999;
				LCD_disp_char(5,2,(Alarm_humidity_low%1000)/100+'0');
				LCD_disp_char(6,2,(Alarm_humidity_low%100)/10+'0');
				LCD_disp_char(7,2,'.');
				LCD_disp_char(8,2,(Alarm_humidity_low%10)+'0');
			}
			if(set_temp_up==1){
				Alarm_temp_up--;
				if(Alarm_temp_up==0)Alarm_temp_up=999;
				LCD_disp_char(5,2,(Alarm_temp_up%1000)/100+'0');
				LCD_disp_char(6,2,(Alarm_temp_up%100)/10+'0');
				LCD_disp_char(7,2,'.');
				LCD_disp_char(8,2,(Alarm_temp_up%10)+'0');
			}
			if(set_humidity_up==1){
				Alarm_humidity_up--;
				if(Alarm_humidity_up==0)Alarm_humidity_up=999;
				LCD_disp_char(5,2,(Alarm_humidity_up%1000)/100+'0');
				LCD_disp_char(6,2,(Alarm_humidity_up%100)/10+'0');
				LCD_disp_char(7,2,'.');
				LCD_disp_char(8,2,(Alarm_humidity_up%10)+'0');
			}
			while(!key_down);
		} 
	}
 }
 void Alarm_Limit(){
 	if(wendu<=Alarm_temp_low){
	 	D1=0;
	 	D2=0;
	 	temp_alarm_flag=0;
	 	TR0=1;
	 	flag=0;
	 	PWMZ=0;
	 }
	 else{}
 	if(wendu>=Alarm_temp_up){
	 	D1=0;
	 	D2=1;
	 	temp_alarm_flag=0;
	 	TR0=1;
	 	flag=1;
	 	PWMF=0;
	 }
	 else{}
	 if(wendu>Alarm_temp_low&&wendu<Alarm_temp_up){
 		D1=1;
	 	D2=1;
	 	temp_alarm_flag=1;
	 	TR0=1;
	 	PWMZ=0;
	 	PWMF=0;
 	}
 	if(shidu<=Alarm_humidity_low){
	 	D3=0;D4=1;
	 	rh_alarm_flag=0;
	 	TR1=1;
	 	flag2=0;
	 	PWMZ2=0;
	 }
	 else{
 		
 	}
 	if(shidu>=Alarm_humidity_up){
	 	D4=0;D3=1;
	 	rh_alarm_flag=0;
	 	TR1=1;
	 	flag2=1;
	 	PWMZ2=0;
	 }
	 else{
 		
 	}
 	if(shidu>Alarm_humidity_low&&shidu<Alarm_humidity_up){
	 	D4=1;D3=1;
	 	rh_alarm_flag=1;
	 	TR1=0;
	 	flag2=1;
	 	PWMZ2=0;
	 	PWMF2=0;
	 }
 	if(temp_alarm_flag==0||rh_alarm_flag==0){
	 	Alarm=0;
	 	delay1ms(10);
	 	Alarm=1;
	 }
	 else{
 		Alarm=1;
 	}
 }
 void SysInit_two(void){
 	TMOD=0x11;
 	TH0=0x3c;
 	TL0=0xb0;
 	TR0=0;
 	ET0=1;
 	TH1=0x3c;
 	TL1=0xB0;
 	TR1=0;
 	ET1=1;
 	EA=1;
 }
 unsigned char time_ms1;
 value humi_val,temp_val;
 unsigned char error,checksum;
 void dis(){
 	error=0;
 	error+=s_measure((unsigned char*)&humi_val.i,&checksum,HUMI);
 	error+=s_measure((unsigned char*)&temp_val.i,&checksum,TEMP);
 	if(error!=0)s_connectionreset();
 	else{
	 	humi_val.f=(float)humi_val.i;
	 	temp_val.f=(float)temp_val.i;
	 	calc_dht90(&humi_val.f,&temp_val.f);
	 	wendu=10*temp_val.f;
	 	LCD_disp_char(8,1,(wendu%1000)/100+'0');
	 	LCD_disp_char(9,1,(wendu%100)/10+'0');
	 	LCD_disp_str(10,1,".");
	 	LCD_disp_char(11,1,(wendu%10)+'0');
	 	LCD_disp_char(12,1,0xdf);
	 	LCD_disp_str(13,1,"C");
	 	shidu=10*humi_val.f;
	 	LCD_disp_char(8,2,(shidu%1000)/100+'0');
	 	LCD_disp_char(9,2,(shidu%100)/10+'0');
	 	LCD_disp_str(10,2,".");
	 	LCD_disp_char(11,2,(shidu%10)+'0');
	 	LCD_disp_str(12,2,"%");
	 	LCD_disp_str(13,2,"R");
	 	LCD_disp_str(14,2,"H");
	 }
 }
 void main(void){
 	LCD_init();
 	SysInit_two();
 	s_connectionreset();
 	LCD_disp_str(0,1,"Temper:     ");
 	LCD_disp_str(0,2,"Humidity:    ");
 	delay_n10us(20000);
 	CYCLE=10;
 	PWM_ON=5;
 	CYCLE2=10;
 	PWM_ON2=5;
 	while(1){
	 	Key_function_scan();
	 	Alarm_Limit();
	 	if(selectnum==5||selectnum==0) dis();
	 }
 }
 void tim(void){
 	static unsigned char count;
 	TH0=(65536-1000)/256;
 	TL0=(65535-1000)%256;
 	if(flag==1){
	 	if(count<=PWM_ON)
	 		PWMZ=1;
 		else
 			PWMZ=1;
	 }
	 if(flag==0){
 		if(count<=PWM_ON)
 			PWMF=1;
		else
			PWMF=0;
 	}
 	count++;
 	if(count==CYCLE){
	 	count=0;
	 }
 }
 void timer1(void){
 	static unsigned char count2;
 	if(flag2==1){
	 	if(count2<=PWM_ON2)
	 		PWMZ2=1;
 		else
 			PWMZ2=0;
	 }
	 if(flag2==0){
	 	if(count2<=PWM_ON2)
	 		PWMZ2=1;
 		else
 			PWMZ2=0;
	 }
	 count2++;
	 if(count2==CYCLE2){
 		count2=0;
 	}
 }