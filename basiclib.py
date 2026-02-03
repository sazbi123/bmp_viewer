def get_data_with_offset(data_list:list,offset:int,size:int)->list:
    # バイトごとに分けられたデータに対してオフセットと取得するデータを指定して返す関数
    return data_list[offset:offset+size]

def get_bits_num(bits:list,little_or_big:int)->int:
    # バイトごとに分けられたデータの値を求め返す関数
    # リトルエンディアンかビッグエンディアンかを第2引数で指定する必要あり
    # little_or_big: 0: little, 1: big
    return_num=0

    if little_or_big==0:
        # little endian
        for i in range(len(bits)):
            # print(bits[i])
            return_num+=bits[i]<<i*8
        
        # print(return_num)
        # print()
        return return_num
    elif little_or_big==1:
        # big endian
        for i in range(len(bits)):
            # print(bits[len(bits)-i-1])
            return_num+=bits[len(bits)-i-1]<<i*8
        
        # print(return_num)
        # print()
        return return_num
    else:
        print("第2引数は0または1です")
        exit()

def byte_num_and_prefix(byte_num:int,SI_or_IEC:int):
    # 単位がバイトのものを適切な接頭語と値に返る関数
    # SI接頭語（キロとか）かIEC（キビとか）を指定する必要がある
    # SI_or_IEC: 0:SI, 1:IEC
    return_byte_num=byte_num
    prefix_SI=["","K","M","G","T"]
    prefix_IEC=["","Ki","Mi","Gi","Ti"]
    prefix_count=0
    if SI_or_IEC==0:
        while True:
            if return_byte_num//1000!=0:
                return_byte_num/=1000
                prefix_count+=1
            else:
                break
        
        try:
            return [return_byte_num,prefix_SI[prefix_count]]
        except IndexError:
            return [return_byte_num,f"10^{prefix_count*3}"]
    elif SI_or_IEC==1:
        while True:
            if return_byte_num//1024!=0:
                return_byte_num/=1024
                prefix_count+=1
            else:
                break
        
        try:
            return [return_byte_num,prefix_IEC[prefix_count]]
        except IndexError:
            return [return_byte_num,f"2^{10*prefix_count}"]
        
def charcode_to_str(char_code:list,little_or_big:int)->str:
    # 文字コードデータリストから文字列を生成する
    # リトルエンディアンかビッグエンディアンかを第2引数で指定する必要あり
    # エンディアンというよりは逆順にするかどうか見たいなこと
    # little_or_big: 0: little, 1: big
    return_str=""

    if little_or_big==0:
        # little endian
        for i in range(len(char_code)):
            return_str+=chr(char_code[len(char_code)-i-1])
    elif little_or_big==1:
        # big endian
        for i in range(len(char_code)):
            return_str+=chr(char_code[i])
    
    return return_str