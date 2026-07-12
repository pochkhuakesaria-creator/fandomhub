from flask import Flask
from app.ext import db, login_manager
from app.routes import bp
from app.models import Fandom


def create_app():

    app = Flask(__name__)

    app.config["SECRET_KEY"] = "secret-key"

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

    db.init_app(app)

    login_manager.init_app(app)

    login_manager.login_view = "main.login"


    app.register_blueprint(bp)


    with app.app_context():

      
        db.create_all()


        # -------- PRE-MADE FANDOMS --------

        if Fandom.query.count() == 0:

            fandoms = [

                Fandom(
                    title="Marvel",
                    category="Movies",
                    description="A community for Marvel fans, superheroes and movies.",
                    image="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Marvel.jpg/1280px-Marvel.jpg"
                ),


                Fandom(
                    title="The Summer Hikaru Died",
                    category="Anime",
                    description="Hikaru vanishes, replaced by an entity with his appearance, voice, and memories. The mysterious being maintains Hikaru's persona, making distinguishing it from the real Hikaru challenging as they continue their daily routines.",
                    image="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSwwWjbxNW5kzRy5qGqQZIwZgwIzbZgKYZR0Bwa_m2kFw&s=10"
                ),


                Fandom(
                    title="My Hero Academia",
                    category="Anime",
                    description="A superhero-admiring boy enrolls in a prestigious hero academy and learns what it really means to be a hero, after the strongest superhero grants him his own powers.",
                    image="https://m.media-amazon.com/images/M/MV5BYTc5NzdjMTQtYTVlMS00ODBlLThlZjctYzYyZTIxZTMxZDJlXkEyXkFqcGc@._V1_QL75_UX244.5_.jpg"
                ),


                Fandom(
                    title="Minecraft",
                    category="Games",
                    description="Share Minecraft builds, ideas and adventures.",
                    image="https://thumbs.dreamstime.com/b/minecraft-game-d-vector-logo-illustration-isolated-white-transparent-banner-background-can-be-used-earth-square-pixels-164066930.jpg"
                ),

                Fandom(
                    title="Bones And All",
                    category="Movies",
                    description="A young woman embarks on a 1000 mile odyssey through America where she meets a disenfranchised drifter. But all roads lead back to their terrifying pasts and to a final stand that will determine whether love can survive their otherness.",
                    image="https://www.rogerebert.com/wp-content/uploads/2024/07/Bones-and-All.jpeg"
                ),

                Fandom(
                    title="Binding Of Issac",
                    category="Video Games",
                    description=" Following Isaac on his journey players will find bizarre treasures that change Isaac’s form giving him super human abilities and enabling him to fight off droves of mysterious creatures, discover secrets and fight his way to safety.",
                    image="https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/113200/header.jpg?t=1643480517"
                ),

                Fandom(
                    title="NEEDY STREAMER OVERLOAD",
                    category="Video Games",
                    description="NEEDY STREAMER OVERLOAD is a “multi-ending ADV” depicting daily life with “OMGkawaiiAngel”, a young girl with a rather extreme need for approval attempting to become the #1 “Internet Angel” (streamer).",
                    image="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQBXQqu1m6mLhcJbOFrlHUXE9IFoY0ZMgOc5txqbcXdqQ&s=10"
                ),

                Fandom(
                    title="The Begginers Guide",
                    category="Video Games",
                    description="The Beginner's Guide is a narrative video game from Davey Wreden, the creator of The Stanley Parable. It lasts about an hour and a half and has no traditional mechanics, no goals or objectives. Instead, it tells the story of a person struggling to deal with something they do not understand.",
                    image="https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/303210/capsule_616x353.jpg?t=1781207118"
                ),

                Fandom(
                    title="Dangarompa",
                    category="Anime",
                    description="Danganronpa is a popular Japanese video game and anime franchise where elite high school students are trapped by a sadistic, mechanical bear named Monokuma.",
                    image="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTiTVDbVqYO_dkK3CTRSObdHDXsd52uzSJIbsWz1QCNxA&s=10"
                )


            ]


            db.session.add_all(fandoms)

            db.session.commit()


    return app
