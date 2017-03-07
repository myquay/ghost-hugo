import os
import json
from datetime import datetime

def main():
    # Read the Ghost export file
    f = open('GhostData.json', encoding="utf8")
    all_posts = json.load(f)['db'][0]['data']['posts']
    f.close()

    for post in all_posts:
        # Create or use a folder for the date
        try:
            created = datetime.utcfromtimestamp(post['created_at']/1000) #, "%Y-%m-%dT%H:%M:%S.000Z")
        except:
            created = datetime.strptime(post['created_at'], "%Y-%m-%d %H:%M:%S")

        if not os.path.exists('./output/%d/%02d/%02d' % (created.year, created.month, created.day)):
            os.makedirs('./output/%d/%02d/%02d' % (created.year, created.month, created.day))

        # Create the Markdown file
        pf = open('./output/%d/%02d/%02d/%s.md' % (created.year, created.month, created.day, post['slug']), 'w', encoding="utf8")

        # Format the permalink
        post['url'] = '/%d/%02d/%02d/%s' % (created.year, created.month, created.day, post['slug'])

        # Front matter
        pf.write('+++\n')
        pf.write('title = "%s"\n' % post['title'].replace('"', '\\"'))
        pf.write('slug = "%s"\n' % post['slug'])
        pf.write('date = "%s"\n' % post['created_at'])
        pf.write('url = "%s"\n' % post['url'])
        if (post['status'] == 'draft'):
            pf.write('draft = true\n')
        pf.write('+++\n\n')

        # Post body
        pf.write(post['markdown'])

        # Close the Markdown file
        pf.close()

if __name__=='__main__':
    main()
