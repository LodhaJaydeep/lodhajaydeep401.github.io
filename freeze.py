from flask_frozen import Freezer
from app import app, list_posts

freezer = Freezer(app)


@freezer.register_generator
def blog_post():
    for post in list_posts():
        yield {'slug': post['slug']}


if __name__ == '__main__':
    freezer.freeze()
