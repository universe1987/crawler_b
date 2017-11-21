import requests


def download(year, school_name, school_num):
    url_template = 'https://www.lsac.org/docs/default-source/official-guide-{}/lsac{}.pdf'
    url = url_template.format(year, school_num)
    resp = requests.get(url)
    print 'year = {}, school_name = {}, school_num = {}'.format(year, school_name, school_num)
    if resp.status_code != 200:
        print resp.content
    if len(resp.content) < 3000:
        print 'no data'
        return False
    if 'pdf' not in resp.content.split('\n')[0].lower():
        print 'bad data'
    with open('data/{}_{}_{}.pdf'.format(year, school_num, school_name), 'wb') as fp:
        fp.write(resp.content)
    return True


def batch_download(year):
    with open('lookup.txt', 'rb') as fp:
        content = [s.strip().split('|') for s in fp.read().split('\n')]
    bad_count = 0
    for row in content:
        school_name, school_num = row
        result = download(year, school_name, school_num)
        if not result:
            bad_count += 1
        else:
            bad_count = 0
        if bad_count > 10:
            break


if __name__ == '__main__':
    for year in range(2017, 1996, -1):
        batch_download(year)
