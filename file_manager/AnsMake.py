import synonyms


def find_answer(input, file_url):
    inputSentence = input
    try:
        CorpusFile = open(file_url, 'r')
    except:
        print("Could not open file")
        return -1
    #inputSentence = CorpusFile.readline()
    pairs = []
    while True:
        lines = CorpusFile.readlines(10000)
        if not lines:
            break
        for line in lines:
            question = line.split()[0]
            ans = line.split()[1]
            pairs.append((question, ans))

    pairs.sort(key=lambda x:synonyms(inputSentence, x[0], seg=True))

    ans = ""
    for i in range(5):
        ans += str(i + 1) + ' ' + pairs[i][1] + '\n'
    #print(ans)
    return ans


def check_file(file):
    File = file
    count = 0
    try:
        while True:
            lines = File.readlines(10000)
            if not lines:
                break
            for line in lines:
                count += 1
                try:
                    question = line.split()[0]
                    answer = line.split()[1]
                except:
                    res = {'code': -1, 'msg': '第' + str(count) + '行格式错误'}
                    return res
    except:
        res = {'code': -1, 'msg': '上传文件格式错误'}
        return res

    res = {'code': 0, 'msg': 'OK'}
    return res
