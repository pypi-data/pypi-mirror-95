import os
import json
from PyQt5.QtWidgets import (QWidget, QGridLayout, QFrame, QLabel, QProgressBar,
                             QPushButton, QFrame, QHBoxLayout, QVBoxLayout,
                             QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QLineEdit)
from PyQt5.QtGui import QFont, QCursor, QIcon, QIntValidator
from PyQt5.QtCore import Qt, QSize, pyqtSlot, pyqtSignal
from fitness_tracker.user_profile.profile_db import fetch_goal, fetch_height, fetch_units, fetch_user_weight, fetch_goal_weight, fetch_age, fetch_gender, fetch_goal_params
from .nutrition_db import create_nutrition_table, fetch_nutrition_data, fetch_calorie_goal, update_calorie_goal
from .change_weight_dialog import ChangeWeightDialog

path = os.path.abspath(os.path.dirname(__file__))
icons_path = os.path.join(path, "icons")

icons = {"pencil": os.path.join(icons_path, "pencil.png"),
         "plus": os.path.join(icons_path, "plus.png"),
         "left": os.path.join(icons_path, "left.png"),
         "right": os.path.join(icons_path, "right.png")}

class NotesPanel(QWidget):
  change_layout_signal = pyqtSignal(str)
  def __init__(self, parent):
    super().__init__(parent)
    create_nutrition_table()
    fetch_nutrition_data()
    self.setStyleSheet(   
    """QWidget{
      color:#c7c7c7;
      font-weight: bold;
      font-family: Montserrat;
      font-size: 16px;
      }
    QPushButton{
      background-color: rgba(0, 0, 0, 0);
      border: 1px solid;
      font-size: 18px;
      font-weight: bold;
      border-color: #808080;
      min-height: 28px;
      white-space:nowrap;
      text-align: left;
      padding-left: 5%;
      font-family: Montserrat;
    }
    QPushButton:hover:!pressed{
      border: 2px solid;
      border-color: #747474;
    }
    QPushButton:pressed{
      border: 2px solid;
      background-color: #323232;
      border-color: #6C6C6C;
    }
    QTableWidget{
      background-color: rgba(135, 41, 41, 20%);  
      border: 0px;
      font-size: 14px;
    }
    QHeaderView:section{
      background-color: rgb(96,58,54);  
      border: 1px solid;
      border-color: #3C2323
    }
    QProgressBar{
      border: 1px solid;
      border-color: #d7d7d7;
      background-color: #d7d7d7;
    }
    QProgressBar:chunk{
      background-color: qlineargradient(x1: 0, y1: 0.5, x2: 1, y2: 0.5, stop: 0 #434343, stop: 1 #440d0f);    
    }
      """)
    self.units = "kg" if fetch_units() == "metric" else "lb"
    self.user_weight = fetch_user_weight()
    self.user_goal_weight = fetch_goal_weight()
    self.goal_parameters = json.loads(fetch_goal_params())
    self.calorie_goal = fetch_calorie_goal()
    self.gender = fetch_gender()
    self.user_height = fetch_height()
    self.user_age = fetch_age()
    self.loss_per_week = self.goal_parameters[1]
    self.user_activity = self.goal_parameters[0]
    self.change_weight_dialog = ChangeWeightDialog()
    self.change_weight_dialog.change_current_weight_signal.connect(lambda weight: self.change_current_weight(weight))
    self.change_weight_dialog.change_goal_weight_signal.connect(lambda weight: self.change_goal_weight(weight))
    self.change_weight_dialog.change_calorie_goal_signal.connect(lambda calorie_goal: self.change_calorie_goal(calorie_goal))
    self.create_panel()
    self.setStyleSheet("QLabel{color:white;}")

  def set_current_layout_button(self, layout):
    if layout == "Food Database":
      self.food_database_button.setStyleSheet("background-color: #603A40;")
      self.notes_button.setStyleSheet("background-color: #191716;")
    elif layout == "Notes":
      self.notes_button.setStyleSheet("background-color: #603A40;")
      self.food_database_button.setStyleSheet("background-color: #191716;")

  @pyqtSlot(str)
  def change_current_weight(self, weight):
    self.current_weight_label.setText(" ".join(["Current Weight:", weight, self.units]))
  
  @pyqtSlot(str)
  def change_goal_weight(self, weight):
    self.goal_weight_label.setText(" ".join(["Current Weight:", weight, self.units]))

  @pyqtSlot(str)
  def change_calorie_goal(self, calorie_goal):
    self.calorie_goal_label.setText(" ".join(["Calorie Goal: \n", calorie_goal]))
    self.progress_bar.setMaximum(int(calorie_goal))
    calories_left = self.progress_bar.maximum() - self.progress_bar.value()
    self.progress_bar.setFormat(" ".join([str(calories_left), "calories left"]))

  def create_panel(self):
    grid = QGridLayout()
    grid.setContentsMargins(2, 0, 8, 8)
    grid.addWidget(self.create_description(), 0, 0, 1, 3)
    #grid.addLayout(self.create_swap_buttons(), 0, 1, 1, 1)
    grid.addLayout(self.create_stats(), 6, 0, 6, 1)
    grid.addWidget(self.create_nutrition_summary(), 6, 1, 6, 1)
    grid.addLayout(self.create_notes(), 16, 0, 10, 3)
    self.setLayout(grid)

  def create_description(self):
    self.description = QLabel("Improve your diet and eating habits by tracking what you eat and searching through our database for healthy \nfood.")
    return self.description

  def create_nutrition_summary(self):
    nsummary_layout = QVBoxLayout()
    daily_monthlyavg_buttons = QHBoxLayout()
    daily_monthlyavg_buttons.addStretch(0)
    dm_style = """
    QPushButton{
      background-color: #440D0F;
      border: 1px solid;
      border-color: #603a36;
    }
    QPushButton:hover:!pressed{
      background-color: #5D1A1D
    }
    QPushButton:pressed{
      background-color: #551812
    }
    """
    dm_style_selected = """"""
    daily_button = QPushButton("Daily")
    daily_button.setFixedWidth(130)
    daily_button.setStyleSheet(dm_style)
    monthly_button = QPushButton("Monthly")
    monthly_button.setFixedWidth(130)
    monthly_button.setStyleSheet(dm_style)
    nutrients_button = QPushButton("Nutrients")
    nutrients_button.setFixedWidth(145)
    daily_monthlyavg_buttons.addWidget(daily_button)
    daily_monthlyavg_buttons.addWidget(monthly_button)
    daily_monthlyavg_buttons.addWidget(nutrients_button)

    nsummary_layout.addLayout(daily_monthlyavg_buttons)
    
    temp_label = QLabel("Proteins: 30g \nCarbs: 300g \nCalories: 2000kcal")
    temp_label.setAlignment(Qt.AlignCenter)
    nsummary_layout.addWidget(temp_label) # Temp

    nsummary_layout_framed = QFrame()
    nsummary_layout_framed.setLayout(nsummary_layout)
    nsummary_layout_framed.setFrameStyle(QFrame.Box)
    nsummary_layout_framed.setLineWidth(3)
    nsummary_layout_framed.setObjectName("frame")
    nsummary_layout_framed.setStyleSheet("""#frame {color: #322d2d;}""")
    return nsummary_layout_framed

  #WIP
  def create_swap_buttons(self):
    buttons_layout = QHBoxLayout()
    self.notes_button = QPushButton("Notes")
    self.notes_button.setStyleSheet("background-color: #603A40;")
    self.notes_button.setFixedSize(60, 35)
    self.notes_button.setCursor(QCursor(Qt.PointingHandCursor))
    self.notes_button.clicked.connect(lambda: self.change_layout_signal.emit(self.notes_button.text()))
    self.food_database_button = QPushButton("Food Database")
    self.food_database_button.setFixedSize(110, 35)
    self.food_database_button.setCursor(QCursor(Qt.PointingHandCursor))
    self.food_database_button.clicked.connect(lambda: self.change_layout_signal.emit(self.food_database_button.text()))
    
    buttons_layout.addWidget(self.notes_button)
    buttons_layout.addWidget(self.food_database_button)
    return buttons_layout

  def create_stats(self):
    stats_layout = QHBoxLayout()
    
    calorie_goal_layout = QVBoxLayout()
    calorie_goal_frame = QFrame()
    self.dci_label = QLabel("Daily Calorie Intake")
    self.dci_label.setAlignment(Qt.AlignCenter)
    self.calorie_goal_label = QLabel(" ".join(["Daily Goal: ", self.calorie_goal, "kcal"]))
    self.calorie_goal_label.setFont(QFont("Ariel", 15))
    self.calorie_goal_label.setAlignment(Qt.AlignCenter)
     
    self.progress_bar = QProgressBar()
    self.progress_bar.setStyleSheet("background-color:grey;")
    self.progress_bar.setMaximum(int(self.calorie_goal))
    self.progress_bar.setValue(500)
    calories_left = self.progress_bar.maximum() - self.progress_bar.value()
    self.progress_bar.setFormat("")
    self.progress_bar.setAlignment(Qt.AlignCenter)
    self.progress_bar.setMaximumHeight(18)
    self.calorie_label = QLabel(str(calories_left) + " calories left from goal")
    self.calorie_label.setAlignment(Qt.AlignCenter)

    intake_button_layout = QHBoxLayout()
    self.calculate_intake = QPushButton("Calculate Daily Intake")
    self.calculate_intake.clicked.connect(lambda: self.calculate_calorie_intake(float(self.user_weight), float(self.user_height), float(self.user_age), self.gender, self.user_activity, self.loss_per_week))
    self.edit_intake = QPushButton("Edit Daily Intake")
    self.edit_intake.clicked.connect(lambda: self.show_intake_entry())
    intake_button_layout.addWidget(self.calculate_intake)
    intake_button_layout.addWidget(self.edit_intake)

    calorie_goal_layout.addWidget(self.dci_label)
    calorie_goal_layout.addWidget(self.progress_bar)
    calorie_goal_layout.addWidget(self.calorie_label)
    calorie_goal_layout.addWidget(self.calorie_goal_label)
    calorie_goal_layout.addLayout(intake_button_layout)

    calorie_goal_frame.setLayout(calorie_goal_layout)
    calorie_goal_frame.setFrameStyle(QFrame.Box)
    calorie_goal_frame.setLineWidth(3)
    calorie_goal_frame.setObjectName("frame")
    calorie_goal_frame.setStyleSheet("""#frame {color: #322d2d;}""")
    stats_layout.addWidget(calorie_goal_frame)

    return stats_layout

  def create_notes(self):
    
    table = QTableWidget(2, 4)
    table.setEditTriggers(QAbstractItemView.NoEditTriggers)
    table.verticalHeader().setVisible(False)
    
    meals = ["Breakfast", "Lunch", "Dinner", "Snacks"]
    
    plus_button = QPushButton(QIcon(icons["plus"]), "Add Food", self)
    plus_button1 = QPushButton(QIcon(icons["plus"]), "Add Food", self)
    plus_button2 = QPushButton(QIcon(icons["plus"]), "Add Food", self)
    plus_button3 = QPushButton(QIcon(icons["plus"]), "Add Food", self)
    
    buttons = [plus_button, plus_button1, plus_button2, plus_button3]
    j = i = 0
    for item in meals:
      buttons[i].setFlat(True)
      table.setHorizontalHeaderItem(i, QTableWidgetItem(item))
      table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
      table.setCellWidget(0, j, buttons[i])
      j += 1
      i += 1

    for i in range(2):
      table.verticalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
        
    table_title_layout = QHBoxLayout()
    style = """QPushButton{background-color: rgba(88, 41, 41, 20%);
               border: 0px solid;
               text-align: center;}
               QPushButton:hover:!pressed {
                 background-color: rgba(120, 55, 55, 20%);
               }
               QPushButton:pressed {
                 background-color: rgba(166, 55, 55, 20%);
               }
             """
    lastweek_button = QPushButton("Last Week")
    lastweek_button.setCursor(QCursor(Qt.PointingHandCursor))
    lastweek_button.setStyleSheet(style)
    thisweek_button = QPushButton("This Week")
    thisweek_button.setStyleSheet(style)
    thisweek_button.setCursor(QCursor(Qt.PointingHandCursor))
    nextweek_button = QPushButton("Next Week")
    nextweek_button.setStyleSheet(style)
    nextweek_button.setCursor(QCursor(Qt.PointingHandCursor))
    manage_meals = QPushButton("Manage Meals")
    manage_meals.setStyleSheet(style)
    manage_meals.setCursor(QCursor(Qt.PointingHandCursor))

    table_title_layout.addWidget(lastweek_button)
    table_title_layout.addWidget(thisweek_button)
    table_title_layout.addWidget(nextweek_button)
    table_title_layout.addWidget(manage_meals)

    table_wrapper = QVBoxLayout()
    table_wrapper.addWidget(table)
    
    grid = QGridLayout()
    grid.setVerticalSpacing(0)
    grid.addLayout(table_title_layout, 0, 0)
    grid.addLayout(table_wrapper, 1, 0)

    framed_grid = QFrame()
    framed_grid.setFrameStyle(QFrame.Box)
    framed_grid.setLineWidth(3)
    framed_grid.setObjectName("frame")
    framed_grid.setStyleSheet("""#frame {color: #322d2d;}""")
    framed_grid.setLayout(grid)

    framed_layout = QVBoxLayout()
    framed_layout.addWidget(framed_grid)
    
    return framed_layout

  def calculate_calorie_intake(self, weight, height, age, gender, activity, weight_goal):
    bmr = self.calculate_bmr(weight, height, age, gender)
    #maintain 100%, 0.25kg/w 90%, 0.5kg/w 79%, 1kg/w 59%
    #"Sedentary", "Lightly active", "Moderately active", "Very active", "Extra active"
    if activity == "Sedentary":
      sedentary_factor = 1.2
      bmr *= sedentary_factor
    elif activity == "Lightly active":
      light_factor = 1.375
      bmr *= light_factor
    elif activity == "Moderately active":
      moderate_factor = 1.465
      bmr *= moderate_factor
    elif activity == "Active":
      active_factor = 1.55
      bmr *= active_factor
    elif activity == "Very active":
      very_active_factor = 1.725
      bmr *= very_active_factor
    elif activity == "Extra active":
      extra_active_factor = 1.9
      bmr *= extra_active_factor
    if weight_goal == "0.25":
      bmr *= 0.9
    elif weight_goal == "0.5":
      bmr *= 0.79
    elif weight_goal == "1":
      bmr *= 0.59
    update_calorie_goal(int(bmr))
    self.calorie_goal = bmr
    self.calorie_goal = int(self.calorie_goal)
    self.calorie_goal = str(self.calorie_goal)
    self.calorie_goal_label.setText(" ".join(["Daily Goal: ", self.calorie_goal, "kcal"]))

  def calculate_bmr(self, weight, height, age, gender):
    #Only calculates base BMR, depending on exercise level, BMR will be multiplied
    #Mifflin-St Jeor Equation
    weight *= 10
    height *= 6.25
    age *= 5
    bmr = weight + height - age
    if gender == "female":
      bmr -= 161
    else:
      bmr += 5
    return int(bmr)

  def show_intake_entry(self):
    global entry
    entry = EditDailyIntake()
    entry.show()

class EditDailyIntake(QWidget):
  def __init__(self):
    super().__init__()

    self.setStyleSheet(   
    """QWidget{
      background-color: #232120;
      color:#c7c7c7;
      font-weight: bold;
      font-family: Montserrat;
      font-size: 16px;
      }
    QPushButton{
      background-color: rgba(0, 0, 0, 0);
      border: 1px solid;
      font-size: 18px;
      font-weight: bold;
      border-color: #808080;
      min-height: 28px;
      white-space:nowrap;
      text-align: left;
      padding-left: 5%;
      font-family: Montserrat;
    }
    QPushButton:hover:!pressed{
      border: 2px solid;
      border-color: #747474;
    }
    QPushButton:pressed{
      border: 2px solid;
      background-color: #323232;
      border-color: #6C6C6C;
    }
    QLineEdit{
      padding: 6px;
      background-color: rgb(33,33,33);
      border: 1px solid;
      border-color: #cdcdcd;
    }""")

    dialog_layout = QVBoxLayout()
    self.setWindowFlags(Qt.FramelessWindowHint)
    dialog_layout.addLayout(self.create_input_window())
    self.setLayout(dialog_layout)

  def create_input_window(self):
    layout = QVBoxLayout()
    entry_label = QLabel("Edit Intake")

    self.calorie_line_edit = QLineEdit()
    self.calorie_line_edit.setValidator(QIntValidator())

    helper_layout = QHBoxLayout()

    cancel_button = QPushButton("Cancel")
    cancel_button.clicked.connect(lambda: self.close_button())

    confirm_button = QPushButton("Confirm")
    confirm_button.clicked.connect(lambda: self.confirm_button())

    helper_layout.addWidget(cancel_button)
    helper_layout.addWidget(confirm_button)

    layout.addWidget(entry_label)
    layout.addWidget(self.calorie_line_edit)
    layout.addLayout(helper_layout)

    return layout

  def close_button(self):
    self.close()

  def confirm_button(self):
    if self.calorie_line_edit.text() != "":
      update_calorie_goal(self.calorie_line_edit.text())
      self.close()
