import re
import requests
import time

LOGIN_URL = 'http://dlfteetime.com/'

def main():
    day = input("Enter \"Sat\" for saturday booking, \"Sun\" for sunday booking: ")
    sat_id = re.compile(re.escape("Fri]</option><option  ")+"value='(.*?)'")
    sun_id = re.compile(re.escape("Sat]</option><option  ")+"value='(.*?)'")
    USERNAME = input('Enter username: ')
    PASSWORD = input('Enter password: ')

    while True:
        if (time.localtime().tm_hour == 16) and (time.localtime().tm_min == 59):
            break

    session_requests = requests.session()

    #Opening Login page
    page = session_requests.get(LOGIN_URL)
    
    #Login details
    payload = {
        'user_id':USERNAME,
        'user_pass':PASSWORD
    }
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    headers['refer'] = LOGIN_URL

    #Logging in
    result = session_requests.post(LOGIN_URL, data = payload, headers = headers)

    
    
    #Simulating Golf Booking click
    id = re.findall(r'pre_shtdet&fx=sht_list&loc_id=(.*?)\\\'>Golf', str(result.content))[0]
    link = 'http://dlfteetime.com/?pg=sht_det&fx=sht_list&loc_id='+id
    while True:
        if (time.localtime().tm_hour == 17) and (time.localtime().tm_min == 00):
            break
    time.sleep(3)
    page = session_requests.get(link)

    #Looking for the new saturday or sunday booking
    if day.lower()=="sat":
        id = re.findall(sat_id, page.text)[0]
    else:
        id = re.findall(sun_id, page.text)[0]
    
    #Updating link with the day added
    link = link+"&sht_id="+id
    day_link = link
    page = session_requests.get(link)

    #extracting the booking link
    booking_re = re.compile("Tee 1<(?:.*?)06:5(?:.)"+"(?:.*?)"+re.escape("</div></td><td class='avail'><div style='width:45px;'><a class='mylink'")+" href='(.*?)'>")
    booking_link = re.findall(booking_re, page.text)[0]
    link = "http://dlfteetime.com/"+booking_link
    
    #loading booking link
    page = session_requests.get(link)


    #form data
    loc_id = re.findall(r"hidden' name='loc_id' value='(.*?)'", page.text)[0]
    sht_id = re.findall(r"hidden' name='sht_id' value='(.*?)'", page.text)[0]
    shtdet_id = re.findall(r"hidden' name='shtdet_id' value='(.*?)'", page.text)[0]
    shtdet_userid = ''
    shtdet_stat = re.findall(r"hidden' name='shtdet_stat' value='(.*?)'", page.text)[0]
    shtdet_tm = re.findall(r"hidden' name='shtdet_tm' value='(.*?)'", page.text)[0]
    sloc_id = re.findall(r"hidden' name='sloc_id' value='(.*?)'", page.text)[0]
    dr_ball = re.findall(r"hidden' name='dr_ball' value='(.*?)'", page.text)[0]
    dr_mem = re.findall(r"hidden' name='dr_mem' value='(.*?)'", page.text)[0]
    dr_guest = re.findall(r"hidden' name='dr_guest' value='(.*?)'", page.text)[0]
    cr_booklmt = re.findall(r"hidden' name='cr_booklmt' value='(.*?)'", page.text)[0]
    mem_id0 = '38294'
    old_mem_id0 = '0'
    mem_id1 = '33393'
    old_mem_id1 = '0'
    mem_id2 = '36829'
    old_mem_id2 = '0'
    mem_id3 = '0'
    old_mem_id3 = '0'
    
    payload = {
        'loc_id':loc_id,
        'sht_id':sht_id,
        'shtdet_id':shtdet_id,
        'shtdet_userid':shtdet_userid,
        'shdet_stat':shtdet_stat,
        'shtdet_tm':shtdet_tm,
        'sloc_id':sloc_id,
        'dr_ball':dr_ball,
        'dr_mem':dr_mem,
        'dr_guest':dr_guest,
        'cr_booklmt':cr_booklmt,
        'mem_id[0]':mem_id0,
        'old_mem_id[0]':old_mem_id0,
        'mem_id[1]':mem_id1,
        'old_mem_id[1]':old_mem_id1,
        'mem_id[2]':mem_id2,
        'old_mem_id[2]':old_mem_id2,
        'mem_id[3]':mem_id3,
        'old_mem_id[3]':old_mem_id3
    }

    headers['refer'] = link
    page = session_requests.post('http://dlfteetime.com/?pg=book&fx=book_post', data = payload, headers = headers)

    page = session_requests.get(day_link)  


if __name__=='__main__':
    main()
