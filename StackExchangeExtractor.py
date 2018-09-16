import xmltodict
import pypandoc

class Posts:
    def __init__(self,id,title):
        self.id = id
        self.title = title
        self.sub_posts = []
    def get_title(self):
        return self.title
    def add_post(self,post):
        self.sub_posts.append(post)
    def get_posts(self):
        return "\n\n\n".join(self.sub_posts)

def parse_dict(doc):
    post_map = {}
    orphan_posts = []
    
    for item in doc['posts']['row']:
        if int(item['@PostTypeId']) == 1:
            p = Posts(int(item['@Id']),str(item['@Title']))
            p.add_post(str(item['@Body']))
            post_map[int(item['@Id'])] = p

        if int(item['@PostTypeId']) == 2:
            if int(item['@ParentId']) in post_map:
                post_map[int(item['@ParentId'])].add_post(str(item['@Body']))
            elif int(item['@ParentId']) not in post_map:
                orphan_posts.append(item)

    for item in orphan_posts:
        if int(item['@ParentId']) in post_map:
            post_map[int(item['@ParentId'])].add_post(str(item['@Body']))

    return post_map

def write_posts_to_file(posts):
    for post in posts:
        title = posts[post].get_title()
        if '/' in title:
            title = title.replace("/","-")
        output = pypandoc.convert_text(title + posts[post].get_posts(),"plain",format='html')
        with open("/home/noah/Media/Documents/Stack Exchange/Devops/" + title + ".txt", "w") as fp:
            fp.write(title)
            fp.write(output)

def main():
    with open("/home/noah/Downloads/devops-exchange/Posts.xml") as fp:
        doc = xmltodict.parse(fp.read())

    posts = parse_dict(doc)
    write_posts_to_file(posts)
    
main()