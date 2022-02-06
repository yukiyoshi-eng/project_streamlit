import streamlit as st
import requests
from PIL import Image,ImageDraw,ImageFont
import io

st.title('顔認識APP')
subscription＿key = 'b113a50ce28743b3a17de31bd9973e57'
assert subscription＿key
face_api_url = 'https://20220127-yuki.cognitiveservices.azure.com/face/v1.0/detect'
headers = {
        'Content-Type':'application/octet-stream',
        'Ocp-Apim-Subscription-Key':subscription＿key
        }
params = {
        'returnFaceId':'true',
        'returnFaceAttributes':'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'
    }
    
uploaded_file = st.file_uploader("Choose an image...",type='jpg')

if uploaded_file is not None :
    img = Image.open(uploaded_file)
    
    exifinfo = img._getexif()
    orientation = exifinfo.get(0x112, 1)
    if orientation == 1:
            pass
    elif orientation == 2:
        #左右反転
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    elif orientation == 3:
        #180度回転
        img = img.transpose(Image.ROTATE_180)
    elif orientation == 4:
        #上下反転
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
    elif orientation == 5:
        #左右反転して90度回転
        img = img.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.ROTATE_90)
    elif orientation == 6:
        #270度回転
        img = img.transpose(Image.ROTATE_270)
    elif orientation == 7:
        #左右反転して270度回転
        img = img.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.ROTATE_270)
    elif orientation == 8:
        #90度回転
        img = img.transpose(Image.ROTATE_90)
    else:
        pass

    with io.BytesIO() as output:
        img.save(output,format='JPEG')
        binary_img = output.getvalue()

    res = requests.post(face_api_url,params=params,headers=headers,data=binary_img)
    results = res.json()

    textcolor = (255, 255, 255)
    textsize = int(img.size[1]/30)
    font = ImageFont.truetype('./arial.ttf',size=textsize)

    for result in results:
        draw = ImageDraw.Draw(img)

        rect = result['faceRectangle']
        draw.rectangle([(rect['left'],rect['top']),(rect['left']+rect['width'],rect['top']+rect['height'])],fill=None,outline='green',width=5)
        
        age = result['faceAttributes']['age']
        gender = result['faceAttributes']['gender']
        text = str(age)+' ' + str(gender)
        txpos = (rect['left'], rect['top']-textsize-10)
        txw, txh = draw.textsize(text, font=font)
        draw.rectangle([txpos, (rect['left']+txw, rect['top'])],outline='green', fill='green', width=5)
        draw.text(txpos, text, font=font, fill=textcolor)
    
    st.image(img,caption='Uploaded Images.',use_column_width=True)
