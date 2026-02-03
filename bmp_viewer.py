# http://www.snap-tck.com/room03/c02/cg/cg02_02.html
# bmpのマルチバイトデータは下位バイトが先に保存されるらしい（リトルエンディアン）
# paddingが課題（特に4bit，1bitの時）
import sys
import tkinter as tk
import basiclib

# def get_data_with_offset(img_data:list,offset:int,size:int)->list:
#     # バイトごとに分けられたデータに対してオフセットと取得するデータを指定して返す関数
#     return img_data[offset:offset+size]

# def get_bits_num(bits:list,little_or_big:int)->int:
#     # バイトごとに分けられたデータの値を求め返す関数
#     # リトルエンディアンかビッグエンディアンかを第2引数で指定する必要あり
#     # little_or_big: 0: little, 1: big
#     return_num=0

#     if little_or_big==0:
#         # little endian
#         for i in range(len(bits)):
#             # print(bits[i])
#             return_num+=bits[i]<<i*8
        
#         # print(return_num)
#         # print()
#         return return_num
#     elif little_or_big==1:
#         # big endian
#         for i in range(len(bits)):
#             # print(bits[len(bits)-i-1])
#             return_num+=bits[len(bits)-i-1]<<i*8
        
#         # print(return_num)
#         # print()
#         return return_num
#     else:
#         print("第2引数は0または1です")
#         exit()

# def byte_num_and_prefix(byte_num:int,SI_or_IEC:int):
#     # 単位がバイトのものを適切な接頭語と値に返る関数
#     # SI接頭語（キロとか）かIEC（キビとか）を指定する必要がある
#     # SI_or_IEC: 0:SI, 1:IEC
#     return_byte_num=byte_num
#     prefix_SI=["B","KB","MB","GB","TB"]
#     prefix_IEC=["B","KiB","MiB","GiB","TiB"]
#     prefix_count=0
#     if SI_or_IEC==0:
#         while True:
#             if return_byte_num//1000!=0:
#                 return_byte_num/=1000
#                 prefix_count+=1
#             else:
#                 break
        
#         return [return_byte_num,prefix_SI[prefix_count]]
#     elif SI_or_IEC==1:
#         while True:
#             if return_byte_num//1024!=0:
#                 return_byte_num/=1024
#                 prefix_count+=1
#             else:
#                 break
        
#         return [return_byte_num,prefix_IEC[prefix_count]]

# def charcode_to_str(char_code:list,little_or_big:int)->str:
#     # 文字コードデータリストから文字列を生成する
#     # リトルエンディアンかビッグエンディアンかを第2引数で指定する必要あり
#     # エンディアンというよりは逆順にするかどうか見たいなこと
#     # little_or_big: 0: little, 1: big
#     return_str=""

#     if little_or_big==0:
#         # little endian
#         for i in range(len(char_code)):
#             return_str+=chr(char_code[len(char_code)-i-1])
#     elif little_or_big==1:
#         # big endian
#         for i in range(len(char_code)):
#             return_str+=chr(char_code[i])
    
#     return return_str

def main():
    argv=sys.argv
    root=tk.Tk()

    if len(argv)<2:
        print("引数が足りません")
        exit()

    try:
        with open(f"./{argv[1]}","rb") as f1:
            image_data=list(f1.read())
    except FileNotFoundError:
        print(f"ファイル{argv[1]}が見つかりません")
        exit()

    bfType=basiclib.charcode_to_str(basiclib.get_data_with_offset(image_data,0,2),1)
    bfSize=basiclib.get_bits_num(basiclib.get_data_with_offset(image_data,2,4),0)
    bfReserved1=basiclib.get_data_with_offset(image_data,6,2)
    bfReserved2=basiclib.get_data_with_offset(image_data,8,2)
    bfOffbits=basiclib.get_bits_num(basiclib.get_data_with_offset(image_data,10,4),0)
    biSize=basiclib.get_bits_num(basiclib.get_data_with_offset(image_data,14,4),0)
    rgbBlue=[]
    rgbGreen=[]
    rgbRed=[]
    rgbReserved=[]

    if biSize==40:
        # Windows
        biWidth=basiclib.get_bits_num(basiclib.get_data_with_offset(image_data,18,4),0)
        biHeight=basiclib.get_bits_num(basiclib.get_data_with_offset(image_data,22,4),0)
        biPlanes=basiclib.get_bits_num(basiclib.get_data_with_offset(image_data,26,2),0)
        biBitCount=basiclib.get_bits_num(basiclib.get_data_with_offset(image_data,28,2),0)
        biCompressin=basiclib.get_bits_num(basiclib.get_data_with_offset(image_data,30,4),0)
        biSizeImage=basiclib.get_bits_num(basiclib.get_data_with_offset(image_data,34,4),0)
        biXPelsPerMeter=basiclib.get_bits_num(basiclib.get_data_with_offset(image_data,38,4),0)
        biYPelsPerMeter=basiclib.get_bits_num(basiclib.get_data_with_offset(image_data,42,4),0)
        biClrUsed=basiclib.get_bits_num(basiclib.get_data_with_offset(image_data,46,4),0)
        biClrImportant=basiclib.get_bits_num(basiclib.get_data_with_offset(image_data,50,4),0)
    elif biSize==12:
        # OS/2
        print("OS/2未実装")
        exit()
    else:
        print("biSizeは未知の値")
        print("または仕様を追い切れていない")
        exit()

    if biBitCount==1 or biBitCount==4 or biBitCount==8:
        entry_num=(bfOffbits-(biSize+14))//4

        for i in range(entry_num):
            rgbBlue.append(basiclib.get_bits_num(basiclib.get_data_with_offset(image_data,biSize+14+i*4,1),0))
            rgbGreen.append(basiclib.get_bits_num(basiclib.get_data_with_offset(image_data,biSize+14+1+i*4,1),0))
            rgbRed.append(basiclib.get_bits_num(basiclib.get_data_with_offset(image_data,biSize+14+2+i*4,1),0))
            rgbReserved.append(basiclib.get_bits_num(basiclib.get_data_with_offset(image_data,biSize+14+3+i*4,1),0))

    with open("./bmp_header_dump.txt","w",encoding="utf8") as f2:
        f2.write(f"bfType={bfType}\nbfSize={bfSize}\nbfReserved1={bfReserved1}\nbfReserved2={bfReserved2}\nbfOffbits={bfOffbits}\nbiSize={biSize}\nbiWidth={biWidth}\nbiHeight={biHeight}\nbiPlanes={biPlanes}\nbiBitCount={biBitCount}\nbiCompressin={biCompressin}\nbiSizeImage={biSizeImage}\nbiXPelsPerMeter={biXPelsPerMeter}\nbiYPelsPerMeter={biYPelsPerMeter}\nbiClrUsed={biClrUsed}\nbiClrImportant={biClrImportant}\nrgbBlue={rgbBlue}\nrgbGreen={rgbGreen}\nrgbRed={rgbRed}\nrgbReserved={rgbReserved}")
    
    row_bytes=int((bfSize-bfOffbits)/biHeight)
    img=tk.PhotoImage(width=biWidth,height=biHeight)

    if biBitCount==1:
        # カラーマップを使うタイプ
        for i in range(biHeight):
            row_data=basiclib.get_data_with_offset(image_data,bfOffbits+row_bytes*i,row_bytes)
            img_row_data=[]

            with open("./bmp_img_data.txt","a",encoding="utf8") as f3:
                f3.write(f"{row_data}\n")
            
            for j in range(biWidth//8):
                px=format(row_data.pop(0),"08b")
                # 7bit目
                r=format(rgbRed[int(px[0],2)],"02x")
                g=format(rgbGreen[int(px[0],2)],"02x")
                b=format(rgbBlue[int(px[0],2)],"02x")
                img_row_data.append(f"#{r}{g}{b}")
                # 6bit目
                r=format(rgbRed[int(px[1],2)],"02x")
                g=format(rgbGreen[int(px[1],2)],"02x")
                b=format(rgbBlue[int(px[1],2)],"02x")
                img_row_data.append(f"#{r}{g}{b}")
                # 5bit目
                r=format(rgbRed[int(px[2],2)],"02x")
                g=format(rgbGreen[int(px[2],2)],"02x")
                b=format(rgbBlue[int(px[2],2)],"02x")
                img_row_data.append(f"#{r}{g}{b}")
                # 4bit目
                r=format(rgbRed[int(px[3],2)],"02x")
                g=format(rgbGreen[int(px[3],2)],"02x")
                b=format(rgbBlue[int(px[3],2)],"02x")
                img_row_data.append(f"#{r}{g}{b}")
                # 3bit目
                r=format(rgbRed[int(px[4],2)],"02x")
                g=format(rgbGreen[int(px[4],2)],"02x")
                b=format(rgbBlue[int(px[4],2)],"02x")
                img_row_data.append(f"#{r}{g}{b}")
                # 2bit目
                r=format(rgbRed[int(px[5],2)],"02x")
                g=format(rgbGreen[int(px[5],2)],"02x")
                b=format(rgbBlue[int(px[5],2)],"02x")
                img_row_data.append(f"#{r}{g}{b}")
                # 1bit目
                r=format(rgbRed[int(px[6],2)],"02x")
                g=format(rgbGreen[int(px[6],2)],"02x")
                b=format(rgbBlue[int(px[6],2)],"02x")
                img_row_data.append(f"#{r}{g}{b}")
                # 0bit目
                r=format(rgbRed[int(px[7],2)],"02x")
                g=format(rgbGreen[int(px[7],2)],"02x")
                b=format(rgbBlue[int(px[7],2)],"02x")
                img_row_data.append(f"#{r}{g}{b}")

            img.put(f"{{{" ".join(img_row_data)}}}",to=(0,biHeight-i-1))
    elif biBitCount==4:
        # カラーマップを使うタイプ
        for i in range(biHeight):
            row_data=basiclib.get_data_with_offset(image_data,bfOffbits+row_bytes*i,row_bytes)
            img_row_data=[]

            with open("./bmp_img_data.txt","a",encoding="utf8") as f3:
                f3.write(f"{row_data}\n")
            
            for j in range(biWidth//2):
                px=format(row_data.pop(0),"08b")
                # 上位4bit
                r=format(rgbRed[int(px[0:4],2)],"02x")
                g=format(rgbGreen[int(px[0:4],2)],"02x")
                b=format(rgbBlue[int(px[0:4],2)],"02x")
                img_row_data.append(f"#{r}{g}{b}")
                # 下位4bit
                r=format(rgbRed[int(px[4:8],2)],"02x")
                g=format(rgbGreen[int(px[4:8],2)],"02x")
                b=format(rgbBlue[int(px[4:8],2)],"02x")
                img_row_data.append(f"#{r}{g}{b}")

            img.put(f"{{{" ".join(img_row_data)}}}",to=(0,biHeight-i-1))
    elif biBitCount==8:
        # カラーマップを使うタイプ
        for i in range(biHeight):
            row_data=basiclib.get_data_with_offset(image_data,bfOffbits+row_bytes*i,row_bytes)
            img_row_data=[]

            with open("./bmp_img_data.txt","a",encoding="utf8") as f3:
                f3.write(f"{row_data}\n")
            
            for j in range(biWidth):
                px=row_data.pop(0)
                r=format(rgbRed[px],"02x")
                g=format(rgbGreen[px],"02x")
                b=format(rgbBlue[px],"02x")
                img_row_data.append(f"#{r}{g}{b}")

            img.put(f"{{{" ".join(img_row_data)}}}",to=(0,biHeight-i-1))
    elif biBitCount==24:
        # ただのRGB
        for i in range(biHeight):
            row_data=basiclib.get_data_with_offset(image_data,bfOffbits+row_bytes*i,row_bytes)
            img_row_data=[]

            with open("./bmp_img_data.txt","a",encoding="utf8") as f3:
                f3.write(f"{row_data}\n")
            
            for j in range(biWidth):
                b=format(row_data.pop(0),"02x")
                g=format(row_data.pop(0),"02x")
                r=format(row_data.pop(0),"02x")
                img_row_data.append(f"#{r}{g}{b}")

            img.put(f"{{{" ".join(img_row_data)}}}",to=(0,biHeight-i-1))
    elif biBitCount==32:
        # 32bitはアルファチャンネルがある
        for i in range(biHeight):
            row_data=basiclib.get_data_with_offset(image_data,bfOffbits+row_bytes*i,row_bytes)
            img_row_data=[]

            with open("./bmp_img_data.txt","a",encoding="utf8") as f3:
                f3.write(f"{row_data}\n")
            
            for j in range(biWidth):
                b=format(row_data.pop(0),"02x")
                g=format(row_data.pop(0),"02x")
                r=format(row_data.pop(0),"02x")
                a=format(row_data.pop(0),"02x")
                img_row_data.append(f"#{r}{g}{b}")

            img.put(f"{{{" ".join(img_row_data)}}}",to=(0,biHeight-i-1))
    else:
        print("壊れたファイルの可能性がある")
        exit()
    
    tk.Label(root, image=img).pack()
    root.mainloop()
    
if __name__=="__main__":
    main()