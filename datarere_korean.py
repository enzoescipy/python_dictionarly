import pickle
with open('kr_korean.csv', 'r',encoding='UTF8') as file:    # hello.txt 파일을 읽기 모드(r)로 열기
    s = file.readlines()
    s = list(map(lambda a : a.split(",")[0],s))
    print(s)

with open('korean.p', 'wb') as file:
    print(pickle.dump(s,file))
