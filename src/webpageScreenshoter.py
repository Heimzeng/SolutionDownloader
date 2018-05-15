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

def wait(driver):
    while True:
        documentState = driver.execute_script('return document.readyState')
        jQueryState = driver.execute_script('return jQuery.active')
        if documentState == 'complete' and jQueryState == 0:
            sleep(1)
            break

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

    # test
    b.driver.get('http://www.chegg.com/homework-help/Digital-Signal-Processing-4th-edition-chapter-2-problem-1P-solution-9780073380490')
    wait(b.driver)
    print('page getted')
    #answerElement = b.driver.find_element_by_id('solution-player-sdk')
    #ol = answerElement.find_element_by_tag_name('ol')
    #chapters = ol.find_elements_by_tag_name('li')
    #chapters_ol = b.driver.find_elements_by_class_name('chapters')
    #chapters_lis = chapters_ol.find_elements_by_class_name('chapter')
    jq_close_chapter_list = '$(".chapter.open h2").click()'
    b.driver.execute_script(jq_close_chapter_list)
    print("close open")
    
    jq_get_chapters_name = 'var chapterNameArray = new Array();                                                     \
                            $(".chapters .chapter").each(function(index){                                           \
                                                             chapterNameArray.push($(this).text());                 \
                                                         });                                                        \
                            return chapterNameArray;                                                                \
                            '
    chapters_name = b.driver.execute_script(jq_get_chapters_name)
    print('chaptersname getted')

    jq_get_problems_names = 'var chapters = new Array();                                                            \
                            $(".chapters .chapter").each(function(index){                                           \
                                                            $(this).find("h2").click();                             \
                                                            var problemElementArray = new Array();                  \
                                                            $(this).find(".problems .problem").each(function(index){\
                                                                problemElementArray.push($(this).text());           \
                                                            });                                                     \
                                                            chapters.push(problemElementArray);                     \
                                                         });                                                        \
                            return chapters;                                                                        \
                            '
    problems_names = b.driver.execute_script(jq_get_problems_names)
    print('problemsname getted')

    for i, chapter_li_i, problems_name in zip(range(len(chapters_name)), chapters_name, problems_names):
        chapter_i_name = chapters_name[i]
        splits = chapter_i_name.split()
        chapter_num = splits[1]
        chapter_i_dir = './solution/chapter' + str(chapter_num) + '/'
        makeDirIfItsNotExist(chapter_i_dir)
        elementId = 'solution-player-sdk'
        for problem_name in problems_name:
            screenshotFilename = problem_name + '.png'
            if not checkFileExist(chapter_i_dir + screenshotFilename):
                print(chapter_i_name, problem_name)
                url = 'http://www.chegg.com/homework-help/Digital-Signal-Processing-4th-edition-chapter-' + str(chapter_num) + '-problem-' + problem_name + '-solution-9780073380490'
                getElementScreenshot(b.driver, url, elementId, 'id', chapter_i_dir, screenshotFilename)
    b.quit()