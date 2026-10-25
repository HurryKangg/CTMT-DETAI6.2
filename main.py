import time
#============================================
# BƯỚC 1: KHỞI TẠO BỘ DỮ LIỆU GIÁ TRỊ
#============================================
#giá trị khởi tạo
values = [
    ("LOAD", "R1", 5),      #address 0
    ("LOAD", "R2", 30),     #address 1
    ("ADD", "R1", 3),       #address 2
    ("SUB", "R1", 5),       #address 3
    ("STORE", "R1", 200),   #address 4
    ("STORE", "R2", 50),    #address 5
    ("SUB", "R1", 1),       #address 6
    ("HALT",),              #address 7
]

# thanh ghi và bộ nhớ data pc (Program Counter) và ir (Instruction Register)
pc = 0                          # Program Counter (PC) khởi tạo nạp lệnh = 0 thì bắt đầu thực thi từ địa chỉ 0
ir = None                       # Intruction Register (IR) chưa có nạp lệnh 
register = {"R1":0 , "R2":0}    # lưu giá trị các thanh ghi
memory_data = []                # tạo bộ nhớ lưu trữ list

#============================================
# BƯỚC 2: NHẬP CHƯƠNG TRÌNh BỘ DỮ LIỆU
#============================================
def parse_lenh(s):
    p = s.replace(",", " ").split()
    return tuple(int(x) if x.isdigit() else x for x in p)

#nhập chương trình
def nhapChuongTrinh():
    '''CHƯƠNG TRÌNH PC, IR'''
    print("----CHƯƠNG TRÌNH----")
    n = 0
    while n < 4 or n > 6:
        n = int(input("Nhập lệnh từ (4-6): "))

    memory = []
    for i in range(n):
        lenh = input(f"[{i}] Nhập lệnh (địa chỉ thứ {i}): ")
        memory.append(parse_lenh(lenh))
    return memory

#============================================
# BƯỚC 3: CÁC BƯỚC THỰC HIỆN LỆNH
#============================================
#các bước step chạy lệnh
def step_print(step, pharse, program):
    print("=" * 60)
    print(f"Bước: {step} | pha {pharse}")               #Bước và pha thực hiện                
    print(f" PC = {pc:>3} (trỏ tới giá trị tiếp theo) ")#Thực hiện PC trỏ tới giá trị tiếp theo của IR
    print(f" IR = {ir if ir is not None else 'RỖNG'}")      #Giá trị IR hiện tại
    print(f" REGISTER = {register}")                    #Thanh ghi được đưa và dict             
    if memory_data:
        print(f" MEMORY DATA = {memory_data}")          #Memory được thêm vào list
    else:                                   
        print(" MEMORY DATA = (đang trống)")            #Memory chưa có dữ liệu
    print("=" * 60)
    time.sleep(0.8)

#============================================
# BƯỚC 4: FETCH - DECODE - EXCUTE
#============================================
def fetch(program):
    global pc,ir
    if pc >= len(program):  #Kiểm tra pc lớn hơn độ dài chương trình cuối cùng 
        return False   #Nếu gặp là False 
    ir = program[pc]   #giá trị IR được đưa vào MEMORY[] VD: pc = 0 -> pro[0]:("LOAD", "R1", 20) -> ir=("LOAD", "R1", 20)
    pc += 1            #Tăng giá trị pc = pc + 1 thực thi lệnh (ADD)
    return True        #Nếu đúng trả về True

def decode(ir):
    opcode = ir[0]     #Đọc phần tử thứ 0 tại list = ("LOAD")

    operands = list(ir[1:])   #Đọc phần tử thứ 1 tại list 1: sẽ chạy tới cuối khi dừng = ("R1", 20)
    return opcode, operands     #Trả về 2 giá trị

def excute(opcode, ops):
    global memory_data
    if opcode == "LOAD": #Nếu là LOAD
        reg,val = ops[0], ops[1]    #Đọc giá trị ("R1", 20) (từ dòng lệnh được lọc ở trên)
        register[reg] = val             #Thêm tại địa chỉ(reg lấy "reg") = (val lấy giá trị 20) cấu trúc (dict[idx] = val)
        return f"{reg} <- {val}"        #Khi đó trả về giá trị reg <- 20 giá trị chèn vào reg
                                
    elif opcode == "ADD":
        reg, val = ops[0], ops[1]     #Đọc giá trị ("R1", 20) (từ dòng lệnh được lọc ở trên)     
        register[reg] +=val                           #Công giá trị khi reg = reg + val
        return f"{reg} <- {reg} + {val} = {register[reg]}" #Trả về reg <- reg + val = ans
    
    elif opcode == "SUB":
        reg, val = ops[0], ops[1]                        #Đọc giá trị ("R1", 20) (từ dòng lệnh được lọc ở trên)     
        register[reg] -= val                  #Trừ giá trị khi reg = reg - val
        return f"{reg} <- {reg} - {val} = {register[reg]}" #Trả về reg <- reg - val = ans
    
    elif opcode == "STORE":
        reg, addr = ops[0], ops[1]                  #Đọc giá trị ("R1", 20) (từ dòng lệnh được lọc ở trên)   
        memory_data.append((addr, register[reg]))     #sử dụng insert(Lưu địa chỉ, lưu giá trị) để xác định của cấu trúc list
        return f"Memory[{addr}] <- {register[reg]}" #trả về Memory[val] <- reg 
    
    elif opcode == "HALT":
        return "Kết thúc chương trình, chúc mừng bạn đã chạy thành công!" #Kết thúc sẽ dừng chương trinh
   
    return "Lệnh không hợp lệ" #Nếu không hợp lệ sẽ báo lỗi và dừng..

#============================================
# BƯỚC 5: MÔ PHỎNG
#============================================   
def moPhong(program):
    global pc,ir
    
    pc = 0
    ir = None
    for k in register:
        register[k] = 0
    memory_data.clear()

    step = 0        #Step các bước 1,2,3,...,n
    halt = False    #Cờ báo hiệu dừng nên default = false
    step_print(step, "INIT", program)
    while pc < len(program) and not halt:
        step+=1
        if not fetch(program):
            break
        step_print(step, "FETCH", program)

        opcode, ops = decode(ir)
        step_print(step, "DECODE", program)

        acc = excute(opcode, ops)
        step_print(step, f"EXCUTE({acc})", program)

        if opcode == "HALT":
            halt = True
        print()

    print(">>>> KẾT THÚC CHƯƠNG TRÌNH")
    print(f">> REGISTER: {register}")
    print(f">> MEMORY DATA: {memory_data}")

#============================================
# BƯỚC 6: CHƯƠNG TRÌNH MAIN
#============================================   
if __name__ == "__main__":
    while True:   # Vòng lặp vô tận để giữ menu
        print("=" * 60)
        print(" MÔ PHỎNG PC & IR TRONG HỆ THỐNG FETCH-DECODE-EXECUTE")
        print("=" * 60)

        chon = input("(1) Nhập tay / (2) Chạy tự động / (0) Thoát: ")

        if chon == "1":
            program = nhapChuongTrinh()      
            moPhong(program)                  
            # Bỏ break ở đây để chạy xong tự về menu
        elif chon == "2":
            program = values
            print(">> CHƯƠNG TRÌNH CHẠY TỰ ĐỘNG")
            for i, l in enumerate(program):
                print(f" [{i}] {l}")
            moPhong(program)
            # Bỏ break ở đây
        elif chon == "0":
            print("Tạm biệt!")
            break     # Chỉ thoát khi người dùng chọn 0
        else:
            print("VUI LÒNG NHẬP LẠI CHƯƠNG TRÌNH!!")