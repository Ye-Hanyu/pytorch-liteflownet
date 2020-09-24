import os 

modeluse = 'default'
path = './input/'
png_path = './out/'
png_out_path = './png_out/'
length = len(os.listdir(path))
num = 0
while (num + 1 < length):
    ml = 'python run.py\t' + '--model\t' + modeluse + '\t--first\t' + path + \
        str(num) + '.png\t' + '--second\t' + path + \
        str(num+1) + '.png\t' + '--out\t' + png_path + str(num+1) + '.flo'
    os.system(ml)
    kl = '~/flow-code/color_flow\t' + png_path + str(num+1) + '.flo\t' + \
        png_out_path + str(num+1) + '.png'
    os.system(kl)
    num += 1
