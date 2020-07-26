from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

engine = create_engine("sqlite:///todo.db?check_same_thread=False")
Base = declarative_base()

class Table(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    task = Column(String, default="default_value")
    deadline = Column(Date, default=datetime.today())

def __repr__(self):
    return self.string_field

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

while True:
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print("5) Add task")
    print("6) Delete task")
    print("0) Exit")
    today = datetime.today().date()
    user_input = int(input())
    if user_input == 1:
        print(f"Today {today.day} {today.strftime('%b')}")
        if session.query(Table).filter(Table.deadline == today).all():
            temp_id = 1
            for entry in session.query(Table).filter(Table.deadline == today).all():
                print(f"{temp_id}. {entry.task}")
                temp_id += 1
        else:
            print("Nothing to do!")
    elif user_input == 2:
        for day in range(7):
            print(f"\n{(today + timedelta(days=day)).strftime('%A')} {(today + timedelta(days=day)).day} {(today + timedelta(days=day)).strftime('%b')}")
            if session.query(Table).filter(Table.deadline == today + timedelta(days=day)).all():
                temp_id = 1
                for entry in session.query(Table).filter(Table.deadline == today + timedelta(days=day)).all():
                    print(f"{temp_id}. {entry.task}\n")
                    temp_id += 1
            else:
                print("Nothing to do!\n")
    elif user_input == 3:
        if session.query(Table).all():
            print("All tasks:")
            for entry in session.query(Table).order_by(Table.deadline).all():
                print(f"{entry.id}. {entry.task}. {entry.deadline.day} {entry.deadline.strftime('%b')}")
        else:
            print("Nothing to do!")
    elif user_input == 4:
        print("Missed Tasks:")
        if session.query(Table).filter(Table.deadline < today).all():
            temp_id = 0
            for entry in session.query(Table).filter(Table.deadline < today).all():
                print(f"{temp_id}. {entry.task}")
                temp_id += 1
            print("\n")
        else:
            print("Nothing is missed!\n")
    elif user_input == 5:
        input_task = input("Enter task")
        input_year, input_month, input_date = map(int, input("Enter deadline").split("-"))
        input_deadline = datetime(input_year, input_month, input_date)
        new_row = Table(task=input_task, deadline=input_deadline)
        session.add(new_row)
        session.commit()
        print("The task has been added!")
    elif user_input == 6:
        print("Choose the number of the task you want to delete:")
        for entry in session.query(Table).order_by(Table.deadline).all():
            print(f"{entry.id}. {entry.task}. {entry.deadline.day} {entry.deadline.strftime('%b')}")
        deletion_number = int(input()) - 1
        tasks = session.query(Table).order_by(Table.deadline).all()
        session.delete(tasks[deletion_number])
        session.commit()
        print("The task has been deleted!\n")

    else:
        print("Bye!")
        exit()
