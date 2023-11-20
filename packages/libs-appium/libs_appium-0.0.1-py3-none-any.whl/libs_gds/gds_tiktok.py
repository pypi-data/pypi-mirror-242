import time
import requests
import logging
from subprocess import check_call

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


logging.basicConfig(level=logging.INFO, format="%(asctime)s.%(msecs)03d [%(levelname)s]: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

class LibsGdsAppium:

    def __init__(self,devices,serverAppium,portAppium):
        self.devices=devices
        self.serverAppium=serverAppium
        self.portAppium=portAppium

        caps = {}
        caps["platformName"] = "Android"
        caps["appium:udid"] = devices.serial

        options = UiAutomator2Options()
        options.load_capabilities(caps)
        self.driver = webdriver.Remote(serverAppium+portAppium+"/wd/hub", options=options)

    def bersihkan_layar(self):
        self.devices.shell(f"adb -s '{self.devices.serial}' forward --remove-all")
        self.driver.terminate_app("com.ss.android.ugc.trill")

    def open_slot(self):
        self.devices.shell('am start -n com.tukanglas.AluminiumMurah/o.ḟ')
        time.sleep(5)


    def open_tiktok(self):
        self.devices.shell('am start -n com.ss.android.ugc.trill/com.ss.android.ugc.aweme.main.MainActivity')
        time.sleep(5)

        self.devices.shell('input keyevent 4') # tombol Back
        time.sleep(1)

        ## ======================================= NOTIF BANGSAT
        try:
            not_batal = WebDriverWait(self.driver, 2).until(
                EC.visibility_of_element_located((By.XPATH, "//android.widget.Button[@text='Cancel']"))
            )
            not_batal.click()
        except:
            logging.info("notif Batal Gak Onk")

        try:
            not_01 = WebDriverWait(self.driver, 2).until(
                EC.visibility_of_element_located((By.XPATH, "//android.widget.Button[@text='Don't allow']"))
            )
            not_01.click()
        except:
            logging.info("notif Jangan izinkan Gak Onk")

        try:
            not_02 = WebDriverWait(self.driver, 2).until(
                EC.visibility_of_element_located((By.XPATH, "//android.widget.Button[@text='Don't allow']"))
            )
            not_02.click()
        except:
            logging.info("notif komunitas panduan gak onok")

        try:
            not_03 = WebDriverWait(self.driver, 2).until(
                EC.visibility_of_element_located((By.XPATH, "//android.widget.Button[@text='Don't allow']"))
            )
            not_03.click()
        except:
            logging.info("notif kkebijakan gak onok")
        ## ======================================= NOTIF BANGSAT

        self.devices.shell('input keyevent 4') # tombol Back
        time.sleep(1)

        try:
            icon_tiktok = WebDriverWait(self.driver, 1).until(
                EC.visibility_of_element_located((By.XPATH, "//android.widget.TextView[@text='Profile']"))
            )
            icon_tiktok.click()
        except:
            logging.info("===== Elemen Profile Gakonok")


        req_ganti_akun   = requests.get("https://sistem.bebitesgroup.com/PROJECT/CPA/api_blast/?action=get_elm_tiktok&id_devices="+self.devices.serial+"&nama_elm=ganti_akun")
        json_ganti_akun  = req_ganti_akun.json()
        res_ganti_akun   = json_ganti_akun[0]["elm_tiktok"]

        self.devices.shell('input touchscreen tap 282 289')  # Click Batal
        self.devices.shell('input touchscreen tap 282 289')  # Click Batal

        try:
            ganti_akun = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, f"{res_ganti_akun}"))
            )
            ganti_akun.click()
        except:
            logging.info(" ******** Err element Ganti Akun")
            self.driver.quit()

    

    def pilih_akun(self,x):
        req_pilih_akun   = requests.get("https://sistem.bebitesgroup.com/PROJECT/CPA/api_blast/?action=get_elm_tiktok&id_devices="+self.devices.serial+"&nama_elm=pilih_akun")
        json_pilih_akun  = req_pilih_akun.json()
        res_pilih_akun   = json_pilih_akun[0]["elm_tiktok"]

        if x <= 2:
            try:
                pilih_akun = WebDriverWait(self.driver, 1).until(
                    EC.visibility_of_element_located((By.XPATH, f"(//android.widget.ImageView[@resource-id='{res_pilih_akun}'])[8]"))
                )
                pilih_akun.click()
            except:
                logging.info(" ******** Err element Pilih Akun")
                self.driver.quit()
        elif x == 3:
            try:
                pilih_akun = WebDriverWait(self.driver, 1).until(
                    EC.visibility_of_element_located((By.XPATH, f"(//android.widget.ImageView[@resource-id='{res_pilih_akun}'])[6]"))
                )
                pilih_akun.click()
            except:
                logging.info(" ******** Err element Pilih Akun")
                self.driver.quit()
        elif x == 4:
            try:
                pilih_akun = WebDriverWait(self.driver, 1).until(
                    EC.visibility_of_element_located((By.XPATH, f"(//android.widget.ImageView[@resource-id='{res_pilih_akun}'])[5]"))
                )
                pilih_akun.click()
            except:
                logging.info(" ******** Err element Pilih Akun")
                self.driver.quit()
        elif x == 5:
            try:
                pilih_akun = WebDriverWait(self.driver, 1).until(
                    EC.visibility_of_element_located((By.XPATH, f"(//android.widget.ImageView[@resource-id='{res_pilih_akun}'])[4]"))
                )
                pilih_akun.click()
            except:
                logging.info(" ******** Err element Pilih Akun")
                self.driver.quit()
        elif x == 6:
            try:
                pilih_akun = WebDriverWait(self.driver, 1).until(
                    EC.visibility_of_element_located((By.XPATH, f"(//android.widget.ImageView[@resource-id='{res_pilih_akun}'])[3]"))
                )
                pilih_akun.click()
            except:
                logging.info(" ******** Err element Pilih Akun")
                self.driver.quit()
        elif x == 7:
            try:
                pilih_akun = WebDriverWait(self.driver, 1).until(
                    EC.visibility_of_element_located((By.XPATH, f"(//android.widget.ImageView[@resource-id='{res_pilih_akun}'])[2]"))
                )
                pilih_akun.click()
            except:
                logging.info(" ******** Err element Pilih Akun")
                self.driver.quit()

        time.sleep(7)
        
    def input_link_music(self):
        req_musik       = requests.get("https://sistem.bebitesgroup.com/PROJECT/CPA/api_blast/?action=get_mst_music")
        json_musik      = req_musik.json()
        link_musik      = json_musik[0]["link_musik"]
        link_musik_01   = link_musik.strip()

        self.driver.execute_script("mobile: deepLink", {'url': f'{link_musik_01}', 'package': 'com.ss.android.ugc.trill'})

        try:
            txt_gunakanSuara = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, "//android.widget.TextView[@text='Use this sound']"))
            )
            txt_gunakanSuara.click()
            logging.info("TOMBOL TENGAH")
        except:
            txt_gunakanSuara = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, "//android.widget.Button[@text='Use this sound']"))
            )
            txt_gunakanSuara.click()
            logging.info("TOMBOL PINGGIR")

        req_btn_play   = requests.get("https://sistem.bebitesgroup.com/PROJECT/CPA/api_blast/?action=get_elm_tiktok&id_devices="+self.devices.serial+"&nama_elm=btn_play")
        json_btn_play  = req_btn_play.json()
        res_btn_play   = json_btn_play[0]["elm_tiktok"]

        try:
            btn_play = WebDriverWait(self.driver, 25).until(
                EC.visibility_of_element_located((By.XPATH, f"(//android.widget.FrameLayout[@resource-id='{res_btn_play}'])[1]"))
            )
            btn_play.click()
        except:
            logging.info(" ******** Err element BTN PLAY")
            self.driver.quit()
        
        try:
            btn_berikutnya = WebDriverWait(self.driver, 40).until(
                EC.visibility_of_element_located((By.XPATH, "//android.widget.TextView[@text='Next']"))
            )
            btn_berikutnya.click()
        except:
            logging.info(" ******** Err element BTN BERIKUTNYA")
            self.driver.quit()

        req_txt_desc   = requests.get("https://sistem.bebitesgroup.com/PROJECT/CPA/api_blast/?action=get_elm_tiktok&id_devices="+self.devices.serial+"&nama_elm=txt_desc")
        json_txt_desc  = req_txt_desc.json()
        res_txt_desc   = json_txt_desc[0]["elm_tiktok"]

        try:
            notif_lokasi_on = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, "//android.widget.Button[@text='OK']"))
            )
            notif_lokasi_on.click()
        except:
            logging.info("NOtif Lokasi Gakonok")


        try:
            txt_desc = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.ID, f"{res_txt_desc}"))
            )
            txt_desc.send_keys("#savepalestine #freepalestine #programmerkuno #gdsbot")
        except:
            logging.info(" ******** Err element TEXT DESC")
            self.driver.quit()

        req_btn_post   = requests.get("https://sistem.bebitesgroup.com/PROJECT/CPA/api_blast/?action=get_elm_tiktok&id_devices="+self.devices.serial+"&nama_elm=btn_post")
        json_btn_post  = req_btn_post.json()
        res_btn_post   = json_btn_post[0]["elm_tiktok"]

        try:
            btn_post = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.ID, f"{res_btn_post}"))
            )
            btn_post.click()
        except:
            logging.info(" ******** Err element BTN POST")
            self.driver.quit()

        try:
            notif_posting_sekarang = WebDriverWait(self.driver, 2).until(
                EC.visibility_of_element_located((By.XPATH, "//android.widget.Button[@text='Confirm']"))
            )
            notif_posting_sekarang.click()
            logging.info("NOtif Posting Saiki ONOK")
        except:
            logging.info("NOtif Posting Saiki Gakonok")

        try:
            notif_posting_sekarang = WebDriverWait(self.driver, 2).until(
                EC.visibility_of_element_located((By.XPATH, "//android.widget.Button[@text='Post Now']"))
            )
            notif_posting_sekarang.click()
            logging.info("NOtif Posting Saiki ONOK")
        except:
            logging.info("NOtif Posting Saiki Gakonok")

        try:
            not_jangan_izinkan = WebDriverWait(self.driver, 2).until(
                EC.visibility_of_element_located((By.XPATH, "//android.widget.Button[@text='Don't allow']"))
            )
            not_jangan_izinkan.click()
        except:
            logging.info("notif Jangan izinkan Gak Onk")

        try:
            not_jangan_izinkan = WebDriverWait(self.driver, 2).until(
                EC.visibility_of_element_located((By.XPATH, "//android.widget.Button[@text='Don't allow']"))
            )
            not_jangan_izinkan.click()
        except:
            logging.info("notif Jangan izinkan Gak Onk")

        self.devices.shell('input keyevent 4') # tombol Back
        time.sleep(2)

    def quit_driver(self):
        self.driver.quit()