import streamlit as st
from PIL import Image, ImageFilter, ImageEnhance
import os
from datetime import datetime

# 깃 연동ㅇㅇ
# 이미지 파일 열어주는 함수
# 이걸 써야 불러온 파일이 열림
def load_image(image_file):
    img = Image.open(image_file)
    return img

# 디렉토리와 이미지를 주면 해당 디렉토리에 이미지를 저장하는 함수
def save_upload_file(directory, img):
    # 1. 디렉토리가 있는지 확인해서 없으면 만든다.
    if not os.path.exists(directory):
        os.makedirs(directory)
    # 2. 이제는 디렉토리가 있으니까 파일을 저장
    file_name = datetime.now().isoformat().replace(':', "-").replace('.','-')
    # 경로설정이므로 / 를 추가해야함
    img.save(directory + '/' + file_name + 'a.jpg')
    return st.success('Saved file : {} in {}'.format(file_name + '.jpg',directory))


def main() :

    print(datetime.now().isoformat())

    st.subheader("이미지 파일 업로드")
    # 이미지 파일 업로드 코드
    image_file_list = st.file_uploader("upload Image", type = ['png','jpg','jpeg'], accept_multiple_files=True)
   
    if image_file_list is not None :
        # 2 각 파일을 이미지로 바꿔줘야함


        image_list = []
        # 2-1 모든 파일이 image_list에 이미지로 저장됨
        for image_file in image_file_list :
            img = load_image(image_file)
            image_list.append(img)
        
        # # 3 이미지 화면에 확인해보자
        # for img in image_list:
        #     st.image(img)

        # 옵션리스트를 화면에 표시하자
        option_list = ['Show Image', 'Rotate Image', 'Create Thumbnail', 
        'Crop Images', 'Merge Image', 'Flip Image', 'Change Color', 
        'Filters - Sharpen', 'Filters - Edge Enhance', 'Contrast Image']

        option = st.selectbox('옵션을 선택하세요', option_list )

        if option == 'Show Image':
            original_img_list = []
            for img in image_list:
                st.image(img)
                original_img_list.append(img)
            derectory = st.text_input('파일경로 입력')
            if st.button('저장'):
                # 3 파일저장
                for img in original_img_list :
                    save_upload_file(derectory, img)
            

        elif option == 'Rotate Image':

            # 1 유저가 입력
            angle = st.slider('각도를 설정하세요', 0,360)
            # 2 모든 이미지를 돌린다.
            transformed_img_list = []
            for img in image_list:
                rotated_img = img.rotate(angle)
                st.image(rotated_img)
                transformed_img_list.append(rotated_img)

            derectory = st.text_input('파일경로 입력')
            if st.button('저장'):
                # 3 파일저장
                for img in transformed_img_list :
                    save_upload_file(derectory, img)



        elif option == 'Create Thumbnail':
            # 원본보다 큰건 예외처리(에러나니까)해야함
            # 먼저 이미지의 사이즈를 알아야겠다.

            # print(img.size)
            width = st.number_input('너비 입력', 1, 100)
            height = st.number_input('높이 입력', 1, 100)

            size = (width, height)

            transformed_img_list = []
            for img in image_list:
                img.thumbnail(size)
                st.image(img)
                transformed_img_list.append(img)
            # 3 파일저장    
            derectory = st.text_input('파일경로 입력')
            if st.button('저장'):
                for img in transformed_img_list :
                    save_upload_file(derectory, img)


        # elif option == 'Crop Images':
        #     # 왼쪽 위부분부터, 너비와 깊이만큼 잘라라
        #     # 왼쪽 위부분 좌표(50,100)
        #     # 너비 x축으로, 깊이 y축으로 (200,200)
        #     start_x = st.number_input('시작 x값', 0, img.size[0]-1)
        #     start_y = st.number_input('시작 y값', 0, img.size[1]-1)
        #     max_width = img.size[0] - start_x
        #     max_height = img.size[1] - start_y
        #     width = st.number_input('너비 입력', 1, max_width)
        #     height = st.number_input('높이 입력', 1, max_height)

        #     box = (start_x, start_y, start_x + width, start_y + height)
        #     cropped_img = img.crop(box)
        #     # cropped_img.save('data/crop.png')
        #     st.image(cropped_img)
        #     # st.image(box)

        # elif option == 'Merge Image' :

        #     merge_file = st.file_uploader('upload Image', type=['png', 'jpg', 
        #                                     'jpeg'], key = 'merge_img')

        #     if merge_img is not None:

        #         merge_img = load_image(merge_file)

        #         start_x = st.number_input('시작 x 좌표', 0, img.size[0]-1)
        #         start_y = st.number_input('시작 y 좌표', 0, img.size[1]-1)     

        #         position = (start_x, start_y)
        #         img.paste(merge_img, position)
        #         st.image(img)
        
        elif option == 'Flip Image' :
            status = st.radio('플립 선택', ['FLIP_TOP_BOTTOM','FLIP_LEFT_RIGHT'])

            if status == "FLIP_TOP_BOTTOM" :
                transformed_img_list = []
                for img in image_list :
                    flipped_img = img.transpose(Image.FLIP_TOP_BOTTOM)
                    st.image(flipped_img)
                    transformed_img_list.append(flipped_img)

            elif status == 'FLIP_LEFT_RIGHT' :
                transformed_img_list = []
                for img in image_list :
                    flipped_img = img.transpose(Image.FLIP_LEFT_RIGHT)
                    st.image(flipped_img)
                    transformed_img_list.append(flipped_img)

            # 저장은 여기서
            directory = st.text_input('파일 경로 입력')
            if st.button('파일 저장') :
                # 파일 저장
                for img in transformed_img_list :
                    save_upload_file(directory, img)


        # elif option == 'Change Color':

        #     status = st.radio('색 변경', ['RGB', 'Gray Scale', 'B & W'])
        #     if status =='RGB':
        #         color = 'RGB'
        #     elif status =='Gray Scale':
        #         color = 'L'
        #     elif status =='B & W':
        #         color = '1'
        #     bw = img.convert(color)
        #     st.image(bw)

        # elif option == 'Filters - Sharpen':
        #     sharp_img = img.filter(ImageFilter.SHARPEN)
        #     st.image(sharp_img)

        # elif option == 'Filters - Edge Enhance' :
        #     edge_img = img.filter(ImageFilter.EDGE_ENHANCE)
        #     st.image(edge_img)

        # elif option == 'Contrast Image' :
        #     contrast_img = ImageEnhance.Contrast(img).enhance(10) # enhance의 단계설정 가능
        #     st.image(contrast_img)

        # 저장시에 유저가 직접 디렉토리 입력하여 저장할수 있도록 만들기


        # st.button('저장하기')
        # direc = st.text_input('저장경로 입력')
        # file_name = img
        # save_upload_file(file_name, direc)
        # st.success('Saved file : {} in {}'.format(file_name, direc))



if __name__ == '__main__' :
    main()
