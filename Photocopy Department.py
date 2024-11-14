import pygame, sys, os, random
from pygame.locals import *
import pandas as pd
import pickle


'''
enter button-settling everything-----over
UX-making the btns bigger when hovered -- over
changing the color of section when hovered -- over
store data directly into excel -- over
'''

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption('Photocopy Department SSSIHL-BRN-Hostel')
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)


res = [800,743+50] #50 for brn moving tag
screen = pygame.display.set_mode(res)
directory = "/materials"
"enter path in the below section for folder items"


#images
bg_img = pygame.image.load('bg_img3.png')
#Radio button
R_off = pygame.transform.scale(pygame.image.load('R_Off.png'),(25,25)).convert_alpha()
R_on = pygame.transform.scale(pygame.image.load('R_On.png'),(25,25)).convert_alpha()
#Click Button
C_off = pygame.transform.scale(pygame.image.load('C_Off.png'),(25,25)).convert_alpha()
C_on = pygame.transform.scale(pygame.image.load('C_On.png'),(25,25)).convert_alpha()


#News displaying pic
instructions_img = pygame.transform.scale(pygame.image.load("information.png"),(750,450))

#Classes/Functions
#Input Box/Text Box
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)
class InputBox():
    def __init__(self, x, y, w, h, text='',active=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = active

    def handle_event(self, event): 
        global player_name_
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            if self.active:
                self.color = COLOR_ACTIVE 
            else:
                self.color = COLOR_INACTIVE

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pygame.K_RETURN:
                    self.text = self.text.__add__('')
                else:
                    self.text += event.unicode


                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)
        #return self.text

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)
        #width = max(200, self.txt_surface.get_width()+10)
        #self.rect.w = width

#Button Class
class Button():
    def __init__(self,x, y, image, scale):
        self.width = image.get_width()
        self.height = image.get_height()
        self.x = x
        self.scale = scale
        self.y = y
        self.btn_img = image
        self.image = pygame.transform.scale(self.btn_img, (int(self.width * self.scale), int(self.height * self.scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.clicked = False

    def draw(self, surface):
        action = False

        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        #not working
        '''
        if pos[0]>self.rect.x and pos[0]<self.rect.x+self.width:
            if pos[1]>self.rect.y and pos[1]<self.rect.y+self.height:
                self.scale+2.3
                self.image = pygame.transform.scale(self.btn_img, (int(self.width * self.scale), int(self.height * self.scale)))
        '''
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #draw button
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action
class Checkbox:
    def __init__(self, surface, x, y, idnum, color=(230, 230, 230),
        caption="", outline_color=(0, 0, 0), check_color=(0, 0, 0),
        font_size=22, font_color=(0, 0, 0),
    text_offset=(28, 1), font='Ariel Black'):
        self.surface = surface
        self.x = x
        self.y = y
        self.color = color
        self.caption = caption
        self.oc = outline_color
        self.cc = check_color
        self.fs = font_size
        self.fc = font_color
        self.to = text_offset
        self.ft = font
        self.R_width = 20
        self.R_height = 20

        #identification for removal and reorginazation
        self.idnum = idnum

        # checkbox object
        self.checkbox_obj = pygame.Rect(self.x, self.y, self.R_width, self.R_height)
        self.checkbox_outline = self.checkbox_obj.copy()

        # variables to test the different states of the checkbox
        self.checked = False

    def _draw_button_text(self): #not using
        self.font = pygame.font.SysFont(self.ft, self.fs)
        self.font_surf = self.font.render(self.caption, True, self.fc)
        w, h = self.font.size(self.caption)
        self.font_pos = (self.x + self.to[0], self.y + 12 / 2 - h / 2 +
        self.to[1])
        self.surface.blit(self.font_surf, self.font_pos)

    def render_checkbox(self):
        if self.checked:
            pygame.draw.rect(self.surface, self.color, self.checkbox_obj)
            pygame.draw.rect(self.surface, self.oc, self.checkbox_outline, 1)
            pygame.draw.circle(self.surface, self.cc, (self.x + 10, self.y + 10), 7)

        elif not self.checked:
            pygame.draw.rect(self.surface, self.color, self.checkbox_obj)
            pygame.draw.rect(self.surface, self.oc, self.checkbox_outline, 1)
        self._draw_button_text()

    def _update(self, event_object):
        x, y = pygame.mouse.get_pos()
        px, py, w, h = self.checkbox_obj
        if px < x < px + w and py < y < py + w:
            if self.checked:
                self.checked = False
            else:
                self.checked = True

    def update_checkbox(self, event_object):
        if event_object.type == pygame.MOUSEBUTTONDOWN:
            self.click = True
            self._update(event_object)


#use this for section highlights
def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)


def append_df_to_excel(df, excel_path):
    df_excel = pd.read_excel(excel_path)
    result = pd.concat([df_excel, df], ignore_index=True)
    result.to_excel(excel_path, index=False)









#3 4 6 7 8
#Object creation
#Section-0
T_Box0 = InputBox(125,15,220,30)#x,y,w,h
T_Box1 = InputBox(155,55,40,30)
T_Box2 = InputBox(530,38,150,30)
#section-1
save_img = pygame.transform.scale(pygame.image.load('save_img.png'),(50,25))
save_button = Button(650,600, save_img, 1)#x,y,image,scale

delete_img = pygame.transform.scale(pygame.image.load('delete_img.png'),(50,25))
#delete_button = Button(650,640, delete_img, 1)

news_img = pygame.transform.scale(pygame.image.load('news_img.png'),(80,40))
info_button = Button(650,680, news_img, 1)

#Section-3
T_Box3 = InputBox(45,453,97,60)
#section-4
T_Box4 = InputBox(310,545,50,30)
#Section-6
T_Box5 = InputBox(585,295,190,70)
#Section-7
T_Box6 = InputBox(460,440,320,130)
#sEction-8
T_Box7 = InputBox(20,635,600,90)

#Checkboxes
#section-1
sec1_boxes=[]
sec1_button = Checkbox(screen, 190, 130, 0, caption='')
sec1_button2 = Checkbox(screen, 360,130, 1, caption='')
sec1_boxes.append(sec1_button)
sec1_boxes.append(sec1_button2)
#section - 2
sec2_boxes=[]
sec2_button = Checkbox(screen, 120,245, 0, caption='')
sec2_button2 = Checkbox(screen, 270,245, 1, caption='')
sec2_button3 = Checkbox(screen, 385,245, 2, caption='')
sec2_boxes.append(sec2_button)
sec2_boxes.append(sec2_button2)
sec2_boxes.append(sec2_button3)
#section - 3
sec3_boxes=[]
sec3_button = Checkbox(screen, 75,345, 0, caption='')
sec3_button2 = Checkbox(screen, 250,360, 1, caption='')
sec3_button3 = Checkbox(screen, 400,360, 2, caption='')
sec3_boxes.append(sec3_button)
sec3_boxes.append(sec3_button2)
sec3_boxes.append(sec3_button3)
#section - 6
sec6_boxes=[]
sec6_button = Checkbox(screen, 525,145, 0, caption='')
sec6_button2 = Checkbox(screen, 670,145, 1, caption='')
sec6_boxes.append(sec6_button)
sec6_boxes.append(sec6_button2)
#section - 7
sec7_boxes=[]
sec7_button = Checkbox(screen, 505,270, 0, caption='')
sec7_button2 = Checkbox(screen, 750,265, 1, caption='')
sec7_boxes.append(sec7_button)
sec7_boxes.append(sec7_button2)


box_highlighted = pygame.transform.scale(pygame.image.load('box.png'),(25,25))

Brn_tag_img = pygame.transform.scale(pygame.image.load('tag.png'), (55,35))
saved_img = pygame.image.load('saved1.png')
Bcolor = (200,200,200,128)


#concat for enter btn and backspace continuos deletion and cursor
#feature of givning permission to locked folder.

#buttons - https://stackoverflow.com/questions/38551168/radio-button-in-pygame
#better text box - https://github.com/Nearoo/pygame-text-input
#add delete btn and save btn
#when the roll no is entered the delete btn will beb available to use and hence delete the entry







#for delete button
def Record_Del(no):
    pass
    ''' thi si not req
    if delete == True:
        os.remove("no".format(no))
    '''



save = False
roll_no = 0
name_created = False
sec1_box = 0
sec2_box = 0
sec3_box = 0
sec6_box = 0
sec7_box = 0
delete = False
seeing_news = False
run = True
t_x=0
t_y=745
data_transfer = False
while run:

    #background
    screen.fill((255,255,255))
    screen.blit(bg_img,(0,0))
    #moving tag
    
        #if t_y > 745 and t_y :
    screen.blit(Brn_tag_img, (t_x,t_y))
    t_x+=8 #speed of the brn
    #t_y+=5
    #if t_x > 0:
        #t_x
    if t_x > 800:
        t_x = 0
    if save_button.draw(screen):
        save = True
    #if delete_button.draw(screen):
        #delete = True




    if not seeing_news:

        seeing_news = info_button.draw(screen)
                        
        #Section - 0
        T_Box0.draw(screen)
        T_Box1.draw(screen)
        T_Box2.draw(screen)

        #Section - 1
        #screen.blit(R_off,(190,130))
        #screen.blit(R_on,(360,130))

        #Section - 2
        #screen.blit(R_on,(120,245))
        #screen.blit(R_on,(270,245))
        #screen.blit(R_on,(385,245))

        #Section - 3
        #screen.blit(R_on,(75,345))
        ##screen.blit(R_on,(250,360))
        #screen.blit(R_on,(400,360))
        T_Box3.draw(screen)

        #Section - 4
        T_Box4.draw(screen)

        #Section - 5
        #screen.blit(R_on,(525,145))
        #screen.blit(R_on,(670,145))


        #Section - 6
        #screen.blit(R_on,(505,270))
        #screen.blit(R_on,(750,265))
        T_Box5.draw(screen)

        #Section - 7
        T_Box6.draw(screen)

        #Section - 8
        T_Box7.draw(screen)

        for box in sec1_boxes:
            box.render_checkbox()
        for box in sec2_boxes:
            box.render_checkbox()
        for box in sec3_boxes:
            box.render_checkbox()
        for box in sec6_boxes:
            box.render_checkbox()
        for box in sec7_boxes:
            box.render_checkbox()

        #chkbx1 - use the rect properties, try t put it after or inside a function
        '''
        pos = pygame.mouse.get_pos()
        if pos[0]>sec1_boxes[0].x and pos[0]<sec1_boxes[0].x+sec1_boxes[0].R_width:
            if pos[1]>sec1_boxes[0].y and pos[1]<sec1_boxes[0].y+sec1_boxes[0].R_height:
                sec1_boxes[0].R_width = 30
                sec1_boxes[0].R_height = 30
        '''
    else:
        screen.fill((0,0,0))
        screen.blit(instructions_img,(0,0))
        seeing_news = True




    #here add all the buttons and text boxes stuff.
    #approx--
    '''
    *no input
    *text input-2(max characters)
    *date - new type of no box(show a sample to enter date, few selected symbols which support excel)

    1. radio buttons - 2
    2. radio buttons - 3
    3. radio buttons - 3 & no input - 1
    4. Number Input
    5. radio buttons - 2
    6. radio buttons - 2 & no box-1(this no btn itself as radio button)
    7. Text Input
    '''
    #after all these
        #store it in pickle file
        #or store it in a separate folder in excel file




















    for event in pygame.event.get():
        #print(event)

        if event.type == pygame.QUIT:
            run=False
        if seeing_news == True:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    seeing_news = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    seeing_news = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            for box in sec1_boxes:
                box.update_checkbox(event)
                if box.checked is True:
                    #box_name = box
                    sec1_box = sec1_boxes.index(box)
                    #print(sec1_box)
                    for b in sec1_boxes:
                        if b != box:
                            b.checked = False
                            #sec1_box = ''
            for box in sec2_boxes:
                box.update_checkbox(event)
                if box.checked is True:
                    #box_name = box
                    sec2_box = sec2_boxes.index(box)
                    #print(sec1_box)
                    for b in sec2_boxes:
                        if b != box:
                            b.checked = False
            for box in sec3_boxes:
                box.update_checkbox(event)
                if box.checked is True:
                    #box_name = box
                    sec3_box = sec3_boxes.index(box)
                    #print(sec1_box)
                    for b in sec3_boxes:
                        if b != box:
                            b.checked = False
            for box in sec6_boxes:
                box.update_checkbox(event)
                if box.checked is True:
                    #box_name = box
                    sec6_box = sec6_boxes.index(box)
                    #print(sec1_box)
                    for b in sec6_boxes:
                        if b != box:
                            b.checked = False
            for box in sec7_boxes:
                box.update_checkbox(event)
                if box.checked is True:
                    #box_name = box
                    sec7_box = sec7_boxes.index(box)
                    #print(sec1_box)
                    for b in sec7_boxes:
                        if b != box:
                            b.checked = False

            #Event handling for all text sec1_boxes
        
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                T_Box0.active = False
                T_Box0.color = COLOR_INACTIVE
                
                T_Box1.active = False
                T_Box1.color = COLOR_INACTIVE
                
                T_Box2.active = False
                T_Box2.color = COLOR_INACTIVE
                
                T_Box3.active = False
                T_Box3.color = COLOR_INACTIVE
                
                T_Box4.active = False
                T_Box4.color = COLOR_INACTIVE
                
                T_Box5.active = False
                T_Box5.color = COLOR_INACTIVE
                
                T_Box6.active = False
                T_Box6.color = COLOR_INACTIVE
                
                T_Box7.active = False
                T_Box7.color = COLOR_INACTIVE
        
        #0
        T_Box0.handle_event(event)
        T_Box1.handle_event(event)
        T_Box2.handle_event(event)
        #3
        T_Box3.handle_event(event)
        #4
        T_Box4.handle_event(event)
        #6
        T_Box5.handle_event(event)
        #7
        T_Box6.handle_event(event)
        #8
        T_Box7.handle_event(event)
        
                


    #coordinates of the check box where the mouse will hover.
    pos = pygame.mouse.get_pos()
    #btn highlight btn1
    if pos[0]>save_button.x and pos[0]<save_button.x+save_button.width:
        if pos[1]>save_button.y and pos[1]<save_button.y+save_button.height:
            save_button.image = pygame.transform.scale(pygame.image.load('save_img.png'),(54,35))
            #self.scale+2.3
            #self.image = pygame.transform.scale(self.btn_img, (int(self.width * self.scale), int(self.height * self.scale)))
    else:
        save_button.image = pygame.transform.scale(pygame.image.load('save_img.png'),(50,25))
    #btn2
    if pos[0]>info_button.x and pos[0]<info_button.x+info_button.width:
        if pos[1]>info_button.y and pos[1]<info_button.y+info_button.height:
            info_button.image = pygame.transform.scale(pygame.image.load('news_img.png'),(54,35
                ))
            #self.scale+2.3
            #self.image = pygame.transform.scale(self.btn_img, (int(self.width * self.scale), int(self.height * self.scale)))
    else:
        info_button.image = pygame.transform.scale(pygame.image.load('news_img.png'),(50,25))
    
    
    
    #wrong
    #box highlight-section-0
    if not seeing_news:
        if pos[0]>0 and pos[0]<800:
            if pos[1]>0 and pos[1]<82:
                draw_rect_alpha(screen, Bcolor, (0, 0, 800, 86))
        '''
        0,0 – 800,82
    12,98 – 433,168 = 421- 70
    12,180 – 433,280  421,100
    13,294 – 433,593  420, 300
    13,533 – 433,580  420, 47
    13,585 – 783,731  770, 146
    453,98 – 784,204  331, 106
    453,214 – 783,376  330, 162
    452,385 – 783,580  330, 195

        ''' 
        #section-1
        if pos[0]>12 and pos[0]<433:
            if pos[1]>98 and pos[1]<168:
                draw_rect_alpha(screen, Bcolor, (12,98, 421, 70))

        #section-2
        if pos[0]>12 and pos[0]<433:
            if pos[1]>180 and pos[1]<280:
                draw_rect_alpha(screen, Bcolor, (12,180, 421, 100))

        #section-3
        if pos[0]>13 and pos[0]<433:
            if pos[1]>294 and pos[1]<593:
                draw_rect_alpha(screen, Bcolor, (13,294, 420, 300))

        #section-4
        if pos[0]>13 and pos[0]<433:
            if pos[1]>533 and pos[1]<580:
                draw_rect_alpha(screen, Bcolor, (13,533, 420, 47))

        #section-5
        if pos[0]>13 and pos[0]<783:
            if pos[1]>585 and pos[1]<731:
                draw_rect_alpha(screen, Bcolor, (13,585, 770, 146))

        #section-6
        if pos[0]>453 and pos[0]<784:
            if pos[1]>98 and pos[1]<204:
                draw_rect_alpha(screen, Bcolor, (453,98, 331, 106))
        
        #section-7
        if pos[0]>453 and pos[0]<784:
            if pos[1]>214 and pos[1]<376:
                draw_rect_alpha(screen, Bcolor, (453,214, 330, 162))
        
        #section-8
        if pos[0]>453 and pos[0]<784:
            if pos[1]>385 and pos[1]<580:
                draw_rect_alpha(screen, Bcolor, (452,385, 330, 195))
            
    else:
        pass
   

    roll_no  = T_Box0.text
    room_no = T_Box1.text
    date = T_Box2.text
    if sec1_box == 0:
        sec_1 ='Photocopy'
    elif sec1_box == 1:
        sec_1 = 'Printout'
    else:
        sec_1 = ''
    #print(sec_1)
    #section - 2
    if sec2_box == 0:
        sec_2 ='Vertical'
    elif sec2_box == 1:
        sec_2 = 'Horizontal'
    elif sec2_box == 2:
        sec_2 = 'As it is'
    else:
        sec_2 = ''
    #section - 3
    if sec3_box == 0:
        sec_3 ='As it is'
    elif sec3_box == 1:
        sec_3 = 'Mini'
    elif sec3_box == 2:
        sec_3 = 'Micro'
    else:
        sec_3 = ''

    PPT_no_cps = T_Box3.text
    copies = T_Box4.text
    sec_5 = T_Box7.text #extra details box
    #section - 6
    if sec6_box == 0:
        sec_6 ='Single side'
    elif sec6_box == 1:
        sec_6 = 'Back to back'
    else:
        sec_6 = ''
    #section - 7
    if sec7_box == 0:
        sec_7 ='All'
    elif sec7_box == 1:
        sec_7 = 'Specific'
    else:
        sec_7 = ''

    pgs_to_print = T_Box5.text
    file_names = T_Box6.text
    #extra_details = T_Box7.text

    #data = pd.Series([roll_no,room_no,date,sec_1,sec_2,sec_3,PPT_no_cps,copies,sec_5,sec_6,pgs_to_print,file_names])#,extra_details])
    #print(data)
        #date format changing
    c = 0
    dd = ''
    for i in range(0,len(date)): 
        if c == 0:
            dd += "".join([date[c]])
        elif c==1:
            dd += "".join([date[c]])
        elif c==2:
            dd += "".join('-')
        elif c == 3:
            dd += "".join([date[c]])
        elif c == 4:
            dd += "".join([date[c]])
        elif c==5:
            dd += "".join('-')
        elif c == 6:
            dd += "".join([date[c]])
        elif c == 7:
            dd += "".join([date[c]])
        elif c == 8:
            dd += "".join([date[c]])
        elif c == 9:
            dd += "".join([date[c]])
        
        c+=1
    date2 = dd










    #all dat will be store in one pandas series.
    #data = roll_no
    #data_index = ['Roll no','Room no','Date','1','2','3','4','5','6','7','8','9']
    #data.index = data_index
    data = {
      "Roll no": [roll_no],
      "Room no": [room_no],
      "Date": [date2],
      "Photocopy/Printout": [sec_1],
      "Page Orientation": [sec_2],
      "Page Layout/PPT Copies": [":~".join([sec_3,PPT_no_cps])],
      "No Of Copies": [copies],
      "Extra Details": [sec_5],
      "Sides To Be Printed": [sec_6],
      "Pages To Be Printed/Pg no": [":~".join([sec_7,pgs_to_print])],
      "Files To Be Printed" : [file_names],
      }
    #df = pd.DataFrame([roll_no,room_no,date,sec_1,sec_2,
                       #"-".join([sec_3,PPT_no_cps]),copies,sec_5,
                       #"-".join([sec_6,pgs_to_print]),file_names])#,extra_details])

    df = pd.DataFrame(data)
    
    
    folder_items = os.listdir()
    if name_created == False:
        r_name = random.randint(1,99)
        #print(r_name)
        if r_name not in folder_items:
            f_name = r_name
            #print(f_name)
        else:
            f_name = random.randint(5,200)
        name_created = True

    if save == True:
        if T_Box0.text != '':
            if data_transfer == False:
                '''
                with pd.ExcelWriter('DATA.xlsx', mode = 'a') as writer:
                    df.to_excel(writer)
                
                
                dat_file = open(str(roll_no), 'wb')
                pickle.dump(data, dat_file) #data dumped in the opened file
                dat_file.close()
                '''
                append_df_to_excel(df, "DATA.xlsx")
                data_transfer = True
    if data_transfer == True:
        screen.blit(saved_img, (300,400))
    #if delete == True:
        #Record_Del(roll_no)
        





    pygame.display.update()
    clock.tick(30)

print(roll_no)
pygame.quit()



