class BANGDIEM:
    '''tinh diem va luu diem trung binh cac mon cua hoc sinh'''
    
    def __init__(self):
        self.monhoc = ('Toan', 'Ly', 'Hoa', 'Sinh', 'Van', 'Anh', 'Su', 'Dia')
        self.montunhien = ('Toan', 'Ly', 'Hoa', 'Sinh')
        self.monxahoi = ('Van', 'Anh', 'Su', 'Dia')

    def load_dulieu(self, file):
        self.file = file
        dauvao  = open(self.file, 'r', encoding = 'utf-8')
        return dauvao.readlines()
        
    def tinhdiem_trungbinh(self):
        lstdiem = self.load_dulieu(self.file)
        self.demuc = lstdiem[0].strip()
        bangdiem = {}
        for line in lstdiem[1:]:
            values = line.strip().split(';')          
            mahs = values[0]
            diemtunhien = []
            diemxahoi = []
            dictdiem = {}
            for diemtn in values[1:5]:
                lstdiemtn = [float(i) for i in diemtn.split(',')]
                trungbinhtn = round(0.05*lstdiemtn[0] + 0.1*lstdiemtn[1] + 0.15*lstdiemtn[2] + 0.7*lstdiemtn[3], 2)
                diemtunhien.append(trungbinhtn)
            for (x1, x2) in zip(self.montunhien, diemtunhien):
                dictdiem[x1] = x2       
            for diemxh in values[5:]:
                lstdiemxh = [float(i) for i in diemxh.split(',')]          
                trungbinhxh = round(0.05*lstdiemxh[0] + 0.1*(lstdiemxh[1] + lstdiemxh[2]) + 0.15*lstdiemxh[3] + 0.6*lstdiemxh[4], 2)
                diemxahoi.append(trungbinhxh)
            for (y1, y2) in zip(self.monxahoi, diemxahoi):
                dictdiem[y1] = y2
            bangdiem[mahs] = dictdiem    
        return bangdiem
                 
    def luudiem_trungbinh(self, daura):
        ghi = open(daura, 'w', encoding = 'utf-8')
        bangdiem = self.tinhdiem_trungbinh()
        ghi.write(self.demuc)
        ghi.write('\n')
        
        for hocsinh in bangdiem.keys():
            ghi.write(hocsinh)
            for i in range(len(self.monhoc)):
                ghi.write(';')
                ghi.write('{:.2f}'.format(bangdiem[hocsinh][self.monhoc[i]]))
            ghi.write('\n')
        
class DANHGIA(BANGDIEM):
    '''danh gia xep loai thi dai hoc'''

    def tinhdiem(self, line):
        values = line.strip().split(';')
        mahs = values[0]
        diem = tuple(float(i) for i in values[1:])
        diemmin = min(diem)
        mon = {}
        for x1, x2 in zip(self.monhoc, diem):
            mon[x1] = x2
        return mon, diem, mahs

    def xeploai_hocsinh(self):
        danhsach = self.load_dulieu(self.file)       
        xeploai = {}       
        for muc in danhsach[1:]:
            mon, diem, mahs = self.tinhdiem(muc)
            diemmin = min(diem)
            diemtb = (mon['Toan'] + mon['Anh'] + mon['Van'] +sum(diem))/11
            if diemtb > 9 and diemmin >= 8:
                xeploai[mahs] = 'Xuat sac'
            elif diemtb > 8 and diemmin >= 6.5:
                xeploai[mahs] = 'Gioi'
            elif diemtb > 6.5 and diemmin >= 5:
                xeploai[mahs] = 'Kha'
            elif diemtb > 6 and diemmin >= 4.5:
                xeploai[mahs] = 'TB Kha'
            else:
                xeploai[mahs] = 'TB'
        return xeploai
    
class TUNHIEN(DANHGIA):
   
    def xeploai_thidaihoc_tunhien(self):
        danhsach = self.load_dulieu(self.file)
        xeploaitunhien = {}       
        for line in danhsach[1:]: 
            mon, diem, mahs = self.tinhdiem(line)
            lst = []
            A = mon['Toan'] + mon['Ly'] + mon['Hoa']
            A1 = mon['Toan'] + mon['Ly'] + mon['Anh']
            B = mon['Toan'] + mon['Hoa'] + mon['Sinh']
            for i in [A, A1, B]:
                if i >= 24:
                    lst.append(1)
                elif i >= 18:
                    lst.append(2)
                elif i >= 12:
                    lst.append(3)    
                else:
                    lst.append(4)
                xeploaitunhien[mahs] = lst
        return xeploaitunhien

class XAHOI(DANHGIA):
   
    def xeploai_thidaihoc_tunhien(self):
        danhsach = self.load_dulieu(self.file)
        xeploaixahoi = {}       
        for line in danhsach[1:]: 
            mon, diem, mahs = self.tinhdiem(line)
            lst = []
            C = mon['Van'] + mon['Su'] + mon['Dia']
                   
            if C >= 21:
                lst.append(1)
            elif C >= 15:
                lst.append(2)
            elif C >= 12:
                lst.append(3)    
            else:
                lst.append(4)                      
            xeploaixahoi[mahs] = lst      
        return xeploaixahoi  
        

class COBAN(DANHGIA):
   
    def xeploai_thidaihoc_tunhien(self):
        danhsach = self.load_dulieu(self.file)
        xeploaicoban = {}       
        for line in danhsach[1:]: 
            mon, diem, mahs = self.tinhdiem(line)
            lst = []
            D = mon['Toan'] + mon['Van'] + mon['Anh']*2

            if D >= 32:
                lst.append(1)
            elif D >= 24:
                lst.append(2)
            elif D >= 20:
                lst.append(3)    
            else:
                lst.append(4)               
            xeploaicoban[mahs] = lst      
        return xeploaicoban  
       
if __name__ == '__main__':

    try:
        a = DANHGIA()
        a.load_dulieu('diem_chitiet.txt')
        output = 'diem_trungbinh.txt'
        a.luudiem_trungbinh(output)
       
        a.load_dulieu('diem_trungbinh.txt')
        xeploai = a.xeploai_hocsinh()
        
        t = TUNHIEN()
        t.load_dulieu('diem_trungbinh.txt')
        tunhien = t.xeploai_thidaihoc_tunhien()

        x = XAHOI()
        x.load_dulieu('diem_trungbinh.txt')
        xahoi = x.xeploai_thidaihoc_tunhien()

        c = COBAN()
        c.load_dulieu('diem_trungbinh.txt')
        coban = c.xeploai_thidaihoc_tunhien()
        
        output = open('danhgia_hocsinh.txt', 'w', encoding = 'utf-8')
        output.write('Ma HS, xeploai_TB chuan, xeploai_A, xeploai_A1, xeploai_B, xeploai_C, xeploai_D')
        output.write('\n')
        for hs in xeploai:
            output.write('{}; {}; {}; {}; {}; {}; {}'.format(hs, xeploai[hs], *tunhien[hs], *xahoi[hs], *coban[hs]))
            output.write('\n')
        output.close()
        
    finally:
        output.close()
    
