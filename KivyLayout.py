def getLayout():
    return '''
<RootWidget>
    BoxLayout:
        spacing: 5.0
        canvas:
            Color:
                rgb: .5,0,.5
        orientation: 'vertical'
        BoxLayout:
            orientation: 'vertical'
            Label:
                text_size: self.size
                halign: 'center'
                size_hint: (1, 0.35)
                padding_x: 35.0
                font_size: 17
                text: 'Click on the Play buttons to hear each sound.\\nTo enable the greyed out buttons, click on the checkboxes next to the Play buttons to select any sounds you like. Test Instrument only takes one selection, but the others take any amount.'
            Label:
                size_hint: (1, 0.7)
                id: notificationLabel
                text: root.notificationLabel 
                font_size: 20
        GridLayout:
            cols: 2
            padding: 7.0
            BoxLayout:
                orientation: 'vertical'
                Label:
                    text: 'Sound 1'
                GridLayout:
                    cols: 4
                    Label:
                        size_hint: (0.20, 1)
                    PlayButton1:
                        size_hint: (0.55, 1)
                    CheckBox1:                       
                        size_hint: (0.14, 1)
                        color: [1, 1, 1, 3]
                    Label:
                        size_hint: (0.06, 1)
            BoxLayout:
                orientation: 'vertical'
                Label:
                    text: 'Sound 2'
                GridLayout:
                    cols: 4
                    Label:
                        size_hint: (0.20, 1)
                    PlayButton2:
                        size_hint: (0.55, 1)
                    CheckBox2:
                        size_hint: (0.14, 1)
                        color: [1, 1, 1, 3]
                    Label:
                        size_hint: (0.06, 1)
            BoxLayout:
                orientation: 'vertical'
                Label:
                    text: 'Sound 3'
                GridLayout:
                    cols: 4
                    Label:
                        size_hint: (0.20, 1)
                    PlayButton3:
                        size_hint: (0.55, 1)
                    CheckBox3:
                        size_hint: (0.14, 1)
                        color: [1, 1, 1, 3]
                    Label:
                        size_hint: (0.06, 1)
            BoxLayout:
                orientation: 'vertical'
                Label:
                    text: 'Sound 4'
                GridLayout:
                    cols: 4
                    Label:
                        size_hint: (0.20, 1)
                    PlayButton4:
                        size_hint: (0.55, 1)
                    CheckBox4:
                        size_hint: (0.14, 1)
                        color: [1, 1, 1, 3]
                    Label:
                        size_hint: (0.06, 1)
            BoxLayout:
                orientation: 'vertical'
                Label:
                    text: 'Sound 5'
                GridLayout:
                    cols: 4
                    Label:
                        size_hint: (0.20, 1)
                    PlayButton5:
                        size_hint: (0.55, 1)
                    CheckBox5:
                        size_hint: (0.14, 1)
                        color: [1, 1, 1, 3]
                    Label:
                        size_hint: (0.06, 1)
            BoxLayout:
                orientation: 'vertical'
                Label:
                    text: 'Sound 6'
                GridLayout:
                    cols: 4
                    Label:
                        size_hint: (0.20, 1)
                    PlayButton6:
                        size_hint: (0.55, 1)
                    CheckBox6:
                        size_hint: (0.14, 1)
                        color: [1, 1, 1, 3]
                    Label:
                        size_hint: (0.06, 1)
        BoxLayout:
            size_hint: (1, .75)
            spacing: 2.0
            GenerateFromSoundsButton:
                id: generateButton
                disabled: root.generateAndSaveDisabled
            RandomizeSoundsButton:
            SaveSoundsButton:
                id: saveButton
                disabled: root.generateAndSaveDisabled
            TestInstrumentButton:
                id: testButton
                disabled: root.testDisabled

<GenerateFromSoundsButton@Button>:      #Inherits from button class
    on_release: app.generateFromSounds()
    disabled: True
    Label:
        text: 'Generate From Sounds'
        center_x: self.parent.center_x
        center_y: self.parent.center_y
        
<RandomizeSoundsButton@Button>:      #Inherits from button class
    on_release: app.randomizeSounds()
    Label:
        text: 'Randomize Sounds'
        center_x: self.parent.center_x
        center_y: self.parent.center_y
        
<SaveSoundsButton@Button>:      #Inherits from button class
    on_press: app.updateNotificationLabelWithoutClear("Saving sounds to desktop...")
    on_release: app.saveSoundsToDesktop()
    disabled: True
    Label:
        text: 'Save Sounds To Desktop'
        center_x: self.parent.center_x
        center_y: self.parent.center_y
    
<TestInstrumentButton@Button>:      #Inherits from button class
    on_press: app.updateNotificationLabelWithoutClear("Preparing sound for playback...")
    on_release: app.testInstrument()
    Label:
        text: 'Test Instrument'
        center_x: self.parent.center_x
        center_y: self.parent.center_y

<PlayButton1@Button>:                       #Inherits from button class
    id: play_button_child
    on_release: app.play_sound(0)
    Label:
        text: 'Play'
        center_x: self.parent.center_x
        center_y: self.parent.center_y
        
<CheckBox1@CheckBox>:
    id: check_box
    on_active: app.on_checkbox_active(self.active, 0)

<PlayButton2@Button>:                       #Inherits from button class
    id: play_button_child
    on_release: app.play_sound(1)
    Label:
        text: 'Play'
        center_x: self.parent.center_x
        center_y: self.parent.center_y

<CheckBox2@CheckBox>:
    id: check_box
    on_active: app.on_checkbox_active(self.active, 1)

<PlayButton3@Button>:                       #Inherits from button class
    id: play_button_child
    on_release: app.play_sound(2)
    Label:
        text: 'Play'
        center_x: self.parent.center_x
        center_y: self.parent.center_y
        
<CheckBox3@CheckBox>:
    id: check_box
    on_active: app.on_checkbox_active(self.active, 2)
		
<PlayButton4@Button>:                       #Inherits from button class
    id: play_button_child
    on_release: app.play_sound(3)
    Label:
        text: 'Play'
        center_x: self.parent.center_x
        center_y: self.parent.center_y
        
<CheckBox4@CheckBox>:
    id: check_box
    on_active: app.on_checkbox_active(self.active, 3)
		
<PlayButton5@Button>:                       #Inherits from button class
    id: play_button_child
    on_release: app.play_sound(4)
    Label:
        text: 'Play'
        center_x: self.parent.center_x
        center_y: self.parent.center_y
        
<CheckBox5@CheckBox>:
    id: check_box
    on_active: app.on_checkbox_active(self.active, 4)
		
<PlayButton6@Button>:                       #Inherits from button class
    id: play_button_child
    on_release: app.play_sound(5)
    Label:
        text: 'Play'
        center_x: self.parent.center_x
        center_y: self.parent.center_y
        
<CheckBox6@CheckBox>:
    id: check_box
    on_active: app.on_checkbox_active(self.active, 5)
'''