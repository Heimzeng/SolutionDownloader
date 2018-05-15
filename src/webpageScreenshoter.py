from splinter.browser import Browser
from time import sleep
import os

def getElementScreenshot(driver, url, elementIdentifier, idType, screenshotDir, screenshotFilename):
    driver.get(url)
    # 模拟滑动鼠标滚轮，加载所有的element
    scheight = .1
    while scheight < 10000:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/%s);" % scheight)
        if scheight < 9.9:
            scheight += .01
        else:
             scheight += 10
    
    while True:
        documentState = driver.execute_script('return document.readyState')
        jQueryState = driver.execute_script('return jQuery.active')
        if documentState == 'complete' and jQueryState == 0:
            break
    if idType == 'id':
        try:
            element = driver.find_element_by_id(elementIdentifier)
        except Exception as e:
            print('cannot find element')
            print(e)
            # raise
        else:
            pass
        finally:
            pass        
    elif idType == 'tag':
        element = driver.find_element_by_tag_name(elementIdentifier)
    element.screenshot(screenshotDir + screenshotFilename)

def makeDirIfItsNotExist(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def checkFileExist(file_path):
    return os.path.isfile(file_path)

if __name__ == '__main__':    
    login_url = 'http://www.chegg.com/login'
    with open('user.txt', 'r') as userFile:
        username = userFile.readline().strip()
        password = userFile.readline().strip()
    isHeadless = True
    b = Browser('firefox', headless=isHeadless)
    b.driver.maximize_window()
    print('entering login page')
    b.driver.get(login_url)
    print('entered login page')
    print('sleep 3')
    sleep(3)
    b.fill("email", username)
    b.fill("password", password)
    print('data filled')
    b.find_by_name(u"login").click()
    print('log in!')
    print('sleep 3')
    sleep(3)
    print('start!')

    P_num =   [0, 53, 66, 81, 91, 85, 106, 69, 35, 49, 50, 45, 60, 53]
    M_num =         [0, 10, 6,  6,  11, 6,  21,  12, 14, 33, 12, 11, 12, 4 ]
    chapter_num = len(P_num)
    for chapter_i_1 in range(chapter_num):
        chapter_i = chapter_i_1 + 1
        P_DIR = './solution/chapter' + str(chapter_i) + '/P/'
        makeDirIfItsNotExist(P_DIR)
        M_DIR = './solution/chapter' + str(chapter_i) + '/M/'
        makeDirIfItsNotExist(M_DIR)
        elementId = 'solution-player-sdk'
        for pro_i_1 in range(P_num[chapter_i_1]):
            pro_i = pro_i_1 + 1
            screenshotFilename = str(pro_i) + 'P' + '.png'
            if not checkFileExist(P_DIR + screenshotFilename):
                print('P:', chapter_i, pro_i)
                url = 'http://www.chegg.com/homework-help/Digital-Signal-Processing-4th-edition-chapter-' + str(chapter_i) + '-problem-' + str(pro_i) + 'P-solution-9780073380490'
                getElementScreenshot(b.driver, url, elementId, 'id', P_DIR, screenshotFilename)
        for m_i_1 in range(M_num[chapter_i_1]):
            m_i = m_i_1 + 1
            screenshotFilename = str(m_i) + 'M' + '.png'
            if not checkFileExist(M_DIR + screenshotFilename):
                print('M:', chapter_i, m_i)
                url = 'http://www.chegg.com/homework-help/Digital-Signal-Processing-4th-edition-chapter-' + str(chapter_i) + '-problem-' + str(m_i) + 'M-solution-9780073380490'
                getElementScreenshot(b.driver, url, elementId, 'id', M_DIR, screenshotFilename)
    b.quit()