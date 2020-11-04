import pickle
with open('words.txt', 'r') as file:    # hello.txt 파일을 읽기 모드(r)로 열기
    s = file.readlines()
    s = list(map(lambda a: a.split("\n")[0], s))

with open('english.p', 'wb') as file:
    pickle.dump(s,file)
