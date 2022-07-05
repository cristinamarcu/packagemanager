import tkinter as tk
from tkinter import ttk
import uuid
import datetime
from PackageManager import DescriptionPackage, PackageManager
from BuildingManager import BuildingManager
from Audit import DescriptionPackageHistory, Audit
from Notification import send_notification
import logging

packageManager = PackageManager()
buildingManager = BuildingManager()
audit = Audit()

window = tk.Tk()
window.title('Package Manager')
style = ttk.Style()
style.configure('My.TFrame', background='red')
frame = ttk.Frame(window, style='My.TFrame')
frame.configure()
tabs = ttk.Notebook(frame)
tab1 = ttk.Frame(tabs)
tab2 = ttk.Frame(tabs)
tab3 = ttk.Frame(tabs)
tab1.grid(rowspan=30, columnspan=30)
tab2.grid()
tab3.grid()
tabs.add(tab1, text='Add')
tabs.add(tab2, text='Check')
tabs.add(tab3, text='Audit')

# tab1

buildinglabeltab1 = ttk.Label(tab1, text='Building')
buildinglabeltab1.grid(row=1, column=1)
apartlabeltab1 = ttk.Label(tab1, text='Apartment')
apartlabeltab1.grid(row=1, column=10)
descriptionlabel = ttk.Label(tab1, text='Description')
descriptionlabel.grid(row=1, column=25)

descript = tk.StringVar()

description = ttk.Entry(tab1, textvariable=descript, width=50)
description.grid(row=6, column=25)


selected_buildingtab1 = tk.StringVar()


def buildingChangedCallbacktab1():
    global selected_buildingtab1

    if selected_buildingtab1.get() in buildingManager.getBuildings():
        chooseAparttab1['values'] = buildingManager.getApartments(selected_buildingtab1.get())


chooseBuildingtab1 = ttk.Combobox(tab1, textvariable=selected_buildingtab1,
                                  values=buildingManager.getBuildings())
chooseBuildingtab1.grid(row=6, column=1)
chooseBuildingtab1.current(0)

selected_aparttab1 = tk.StringVar()
chooseAparttab1 = ttk.Combobox(tab1, textvariable=selected_aparttab1,
                               values=buildingManager.getApartments(buildingManager.getBuildings()[0]),
                               postcommand=buildingChangedCallbacktab1)
chooseAparttab1.grid(row=6, column=10)
chooseAparttab1.current(0)


def enter_clicked(descr: str):
    item = DescriptionPackage(selected_buildingtab1.get(), selected_aparttab1.get(), str(datetime.datetime.now()),
                              description.get(),
                              str(uuid.uuid1().int))
    packageManager.addPackage(item)
    itemHistory = DescriptionPackageHistory(item, "RECEIVED")
    infoapart = buildingManager.getApartmentInfo(item.building, item.apartment)
    validreceived=send_notification(infoapart.email, item.apartment, infoapart.name, item.description, item.date, itemHistory.action)
    if validreceived==False:
        result_label_received = ttk.Label(tab1, text='Notification not sent. No internet connection')
        result_label_received.grid(row=30, column=1)

    audit.addToHistory(itemHistory)
    description.delete(0, 'end')


description.bind('<Return>', enter_clicked)


def addpackageclicked():
    return enter_clicked(description.get())


buttonAdd = ttk.Button(tab1, text='Add')
buttonAdd.grid(row=23, column=10)
buttonAdd.configure(command=addpackageclicked)

# tab2
buildinglabeltab2 = ttk.Label(tab2, text='Building')
buildinglabeltab2.grid(row=1, column=1)
selected_buildingtab2 = tk.StringVar()

apartlabeltab2 = ttk.Label(tab2, text='Apartment')
apartlabeltab2.grid(row=1, column=10)


def buildingChangedCallbacktab2():
    global selected_buildingtab2

    if selected_buildingtab2.get() in buildingManager.getBuildings():
        chooseAparttab2['values'] = buildingManager.getApartments(selected_buildingtab2.get())


chooseBuildingtab2 = ttk.Combobox(tab2, textvariable=selected_buildingtab2,
                                  values=buildingManager.getBuildings())
chooseBuildingtab2.grid(row=6, column=1)
chooseBuildingtab2.current(0)

selected_aparttab2 = tk.StringVar()
chooseAparttab2 = ttk.Combobox(tab2, textvariable=selected_aparttab2,
                               values=buildingManager.getApartments(buildingManager.getBuildings()[0]),
                               postcommand=buildingChangedCallbacktab2)
chooseAparttab2.grid(row=6, column=10)
chooseAparttab2.current(0)
checkbutton = ttk.Label(tab2, text='CheckPackage')
checkbutton.grid(row=10, column=1)

gobuttontab2 = ttk.Button(tab2, text='Go')
gobuttontab2.grid(row=6, column=20)
deletebutton = ttk.Button(tab2, text='Delete')
deletebutton.grid(row=20, column=10)
returnbutton = ttk.Button(tab2, text='Return')
returnbutton.grid(row=20, column=15)

columns = ('date', 'description', 'id')
listpackage = ttk.Treeview(tab2, columns=columns, show='headings')
listpackage.grid(row=11, column=1)
listpackage.heading('date', text='date')
listpackage.heading('description', text='description')
listpackage.heading('id', text='id')
listpackage.column('id', minwidth=0, width=0)
verscrlbar = ttk.Scrollbar(tab2, orient=tk.VERTICAL)
verscrlbar.configure(command=listpackage.yview)
verscrlbar.grid(row=11, column=2, sticky=tk.NS)
listpackage.configure(yscrollcommand=verscrlbar.set)


def checkpackageclicked():
    for item in listpackage.get_children():
        listpackage.delete(item)
    elemlist = []
    for package in packageManager.getPackages(selected_buildingtab2.get(), selected_aparttab2.get()):
        elemlist.append([package.date, package.description, package.id])
    for elem in elemlist:
        listpackage.insert('', tk.END, values=[elem[0], elem[1], elem[2]])
        print(elem[2])


def getItem() -> list:
    for selected_item in listpackage.selection():
        print(selected_item)
        print(listpackage.item(selected_item))
        selected_id = str(listpackage.item(selected_item)["values"][2])
        listpackage.delete(selected_item)
        item = packageManager.getPackage(selected_id)
        return [item, selected_id]


def delete_button_clicked():
    item = getItem()
    itemHistory = DescriptionPackageHistory(item[0], 'PICKED_UP')
    audit.addToHistory(itemHistory)
    infoapartpicked = buildingManager.getApartmentInfo(item[0].building, item[0].apartment)
    validPicked=send_notification(infoapartpicked.email, item[0].apartment, infoapartpicked.name, item[0].description, item[0].date,
                      itemHistory.action)
    if validPicked==False:
        result_label_picked = ttk.Label(tab2,text='Notification not sent. No internet connection')
        result_label_picked.grid(rowspan=25, columnspan=10)

    packageManager.deletePackage(item[1])


def return_button_clicked():
    item = getItem()
    itemHistory = DescriptionPackageHistory(item[0], 'RETURNED')
    audit.addToHistory(itemHistory)
    infoapartreturned = buildingManager.getApartmentInfo(item[0].building, item[0].apartment)
    validReturned=send_notification(infoapartreturned.email, item[0].apartment, infoapartreturned.name, item[0].description,
                      item[0].date, itemHistory.action)
    if validReturned==False:
        result_label_returned = ttk.Label(tab2,text='Notification not sent. No internet connection')
        result_label_returned.grid(rowspan=25, columnspan=10)
    packageManager.deletePackage(item[1])


gobuttontab2.configure(command=checkpackageclicked)
deletebutton.configure(command=delete_button_clicked)
returnbutton.configure(command=return_button_clicked)

# tab3
buildinglabeltab3 = ttk.Label(tab3, text='Building')
buildinglabeltab3.grid(row=1, column=0)
selected_buildingtab3 = tk.StringVar()

apartlabeltab3 = ttk.Label(tab3, text='Apartment')
apartlabeltab3.grid(row=1, column=4)


def buildingChangedCallbacktab3():
    global selected_buildingtab3

    if selected_buildingtab3.get() in buildingManager.getBuildings():
        chooseAparttab3['values'] = buildingManager.getApartments(selected_buildingtab3.get())


chooseBuildingtab3 = ttk.Combobox(tab3, textvariable=selected_buildingtab3,
                                  values=buildingManager.getBuildings())
chooseBuildingtab3.grid(row=6, column=0)
chooseBuildingtab3.current(0)

selected_aparttab3 = tk.StringVar()
chooseAparttab3 = ttk.Combobox(tab3, textvariable=selected_aparttab3,
                               values=buildingManager.getApartments(buildingManager.getBuildings()[0]),
                               postcommand=buildingChangedCallbacktab3)
chooseAparttab3.grid(row=6, column=4)
chooseAparttab3.current(0)
checkbuttontab3 = ttk.Label(tab3, text='PackageHistory')
checkbuttontab3.grid(row=10, column=0)

gobuttonaudit = ttk.Button(tab3, text='Go')
gobuttonaudit.grid(row=6, column=13)

columns = ('date', 'description', 'id', 'action')
listpackageaudit = ttk.Treeview(tab3, columns=columns, show='headings')
listpackageaudit.grid(row=11, column=0)
listpackageaudit.heading('date', text='date')
listpackageaudit.heading('description', text='description')
listpackageaudit.heading('id', text='id')
listpackageaudit.heading('action', text='action')
listpackageaudit.column('id', minwidth=0, width=0)
verscrlbaraudit = ttk.Scrollbar(tab3, orient=tk.VERTICAL)
verscrlbaraudit.configure(command=listpackageaudit.yview)
verscrlbaraudit.grid(row=11, column=2, sticky=tk.NS)
listpackageaudit.configure(yscrollcommand=verscrlbaraudit.set)


def checkpackageclickedaudit():
    for item in listpackageaudit.get_children():
        listpackageaudit.delete(item)
    elemlist = []
    for info in audit.getPackageHistory(selected_buildingtab3.get(), selected_aparttab3.get()):
        elemlist.append([info.package.date, info.package.description, info.package.id, info.action])
    for elem in elemlist:
        listpackageaudit.insert('', tk.END, values=[elem[0], elem[1], elem[2], elem[3]])


gobuttonaudit.configure(command=checkpackageclickedaudit)
logging.basicConfig(level=logging.INFO)
tabs.grid(padx=10, pady=10, rowspan=20, columnspan=20)
frame.pack(expand=True, fill='both')
window.mainloop()
