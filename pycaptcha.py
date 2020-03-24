# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 14:17:33 2020

@author: jfpd1764
"""
import pytesseract as pyst
import sys
import argparse
from PIL import Image
from subprocess import check_output
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import pandas as pd
import os
import urllib.request
import time
#from selenium import webdriver

##important to first install tesseract

pyst.pytesseract.tesseract_cmd = 'PATH_TO_tesseract.exe'


def resolve2(img_sel):
    captcha_text= pyst.image_to_string(img_sel)
    return(captcha_text)

##path to your webdriver
webdr = "PATH_TO_chromedriver.exe"

driver = Chrome(webdr)

def get_captcha(driver, element, path):
    # now that we have the preliminary stuff out of the way time to get that image :D
    location = element.location
    size = element.size
    # saves screenshot of entire page
    
    if os.path.exists(path+"screen.jpg"):
        os.remove(path+"screen.jpg")
        driver.save_screenshot(path+"screen.jpg")
    else:
        driver.save_screenshot(path+"screen.jpg")

    # uses PIL library to open image in memory
    
    
    image = Image.open(path+"screen.jpg").convert("L")
    #image.show()
    left = location['x']+10
    bottom = location['y'] + size['height']-6
    right = location['x'] + size['width']-20
    top = location['y']+6


    image2 = image.crop((left, top, right, bottom)) 
    #image2.show()
    #image=image.convert('RGB')# defines crop points
    return(resolve2(image2))    

#img = driver.find_element_by_id("capimg")
#img= driver.find_element_by_xpath("//img[contains(@id,'capimg')]")
#get_captcha(driver,element=img, path="C:/Users/jfpd1764/Desktop/captcha/")


def access_antecedentes(ced="YOUR_ID_BY_DEFAULT",path_aux="AUX_PATH_TO_SAVE_CAPTCHA_SCREENSHOT",silent=False):
    """
    ced: Cédula de Ciudadanía Colombiana
    path_aux: destino de imágnes auxiliares a guardar
    silent: si se desea el navegador minimizado o no: por default se asume como False
    """
    
    driver = Chrome(webdr)

    ## Abrir Navegador
    url="https://antecedentes.policia.gov.co:7005/WebJudicial/"
    driver.get(url)
    if silent: driver.minimize_window()
    
    time.sleep(3)
    ## seleccionar que si acepta los términos
    
    try:
        driver.find_element_by_class_name("close").click()
        time.sleep(2)
    except: Exception
    
    
    
    driver.find_element_by_css_selector("input[type='radio'][value='true']").click()
    time.sleep(1)
       
    
    ## seleccionar el botón de continuar
    driver.find_element_by_id('continuarBtn').click()
    time.sleep(2)
    ## obtener imágen del captcha
    img= driver.find_element_by_xpath("//img[contains(@id,'capimg')]")
    ## llenar con la cédula
    cedula=driver.find_element_by_id("cedulaInput")
    cedula.send_keys(ced)
    ## llenar el captcha
        
    ##continuar hasta que tenga éxito en el captcha
    out_id=False
    while(out_id==False):
        time.sleep(2)
        try:
            ##si falla que lo vuelva a intentar: se repite el proceso de obtener la imágen
            img= driver.find_element_by_xpath("//img[contains(@id,'capimg')]")
            captcha_input=driver.find_element_by_id("textcaptcha")
            captcha_input.send_keys(get_captcha(driver,img,path=path_aux))
            send_button=driver.find_element_by_name("j_idt20")
            send_button.click()
            time.sleep(2)
            textof=driver.find_element_by_id("form:mensajeCiudadano")
            nombre=textof.text.split(ced)[1].split("\n")[1][21::]
            print(f"Éxito encontrando {ced}:{nombre}")
            out_id=True
        except:
            print("error en captcha, reintentando...")  
        
    ##sacar texto con el nombre
    ##cerrar navegador
    driver.close()
    return(nombre)
    
    
access_antecedentes(ced="YOUR_ID_HERE",silent=False)
        

