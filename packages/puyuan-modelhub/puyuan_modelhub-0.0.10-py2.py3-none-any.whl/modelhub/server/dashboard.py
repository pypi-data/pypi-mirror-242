import gradio as gr
import pymongo
import pandas as pd
from utils import hash_password
import yaml
import logging
import uvicorn

config, logger, messages_collection, users_collection = None, None, None, None


def setup_env():
    global config, logger, messages_collection, users_collection
    try:
        config = yaml.safe_load(open("/home/whx/modelhub/config.yml"))
        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            level=logging.INFO,
        )
        logger = logging.getLogger(__name__)
        client = pymongo.MongoClient(config["MONGO_URL"])
        db = client["llm-api"]
        messages_collection = db["messages"]
        users_collection = db["users"]
        print("Connected to MongoDB")
    except Exception as e:
        print("Error setting up env", e)


items_per_page = 20
start_page = 0


def get_messages(page, items_per_page):
    global messages_collection
    logging.info(f"get_messages: page={page}, items_per_page={items_per_page}")
    messages = list(
        messages_collection.find(
            projection={"_id": 0, "message_id": 0},
            skip=page * items_per_page,
            limit=items_per_page,
            sort=[("_id", -1)],
        )
    )

    def truncate(s: str, decode=False):
        if len(s) > 200:
            return s[:50] + "..." + s[-50:]
        if decode:
            return s
        return s

    for message in messages:
        message["parameters"] = truncate(str(message.get("parameters", {})))
        message["prompt"] = truncate(message["prompt"])
        message["response"] = truncate(message["response"], True)
    return pd.DataFrame(messages)


def update_messages(page, iterms_per_page):
    messages = get_messages(page, iterms_per_page)
    return gr.DataFrame(value=messages)


def get_users():
    global users_collection
    logging.info(f"get_users")
    users = list(users_collection.find(projection={"_id": 0}))
    return users


def delete_user(user_name):
    global users_collection
    logging.info(f"delete_user: user_name={user_name}")
    users_collection.delete_one({"_id": user_name})


def add_user(user_name, password):
    global users_collection
    logging.info(f"add_user: user_name={user_name}, password={password}")
    users_collection.insert_one(
        {"_id": user_name, "user_name": user_name, "password": hash_password(password)}
    )


def update_user(user_name, password):
    global users_collection
    logging.info(f"update_user: user_name={user_name}, password={password}")
    users_collection.update_one(
        {"_id": user_name},
        {"$set": {"user_name": user_name, "password": hash_password(password)}},
    )


with gr.Blocks(title="Puyuan Model Hub") as demo:
    setup_env()
    with gr.Tab("Chat Logs"):
        with gr.Column(variant="panel"):
            gr.Markdown("## Chat Logs")
            with gr.Row():
                ipp = gr.Number(items_per_page, label="Iterms per page", precision=0)
                page = gr.Number(start_page, label="Page", precision=0)
                refresh_btn = gr.Button("Refresh")
                previous_btn = gr.Button("Previous Page")
                next_btn = gr.Button("Next Page")
            log_table = gr.Dataframe(get_messages(start_page, items_per_page))
            next_btn.click(
                lambda page, ipp: get_messages(page + 1, ipp),
                inputs=[page, ipp],
                outputs=[log_table],
            ).then(lambda page: page + 1, inputs=[page], outputs=[page])
            previous_btn.click(
                lambda page, ipp: get_messages(page - 1 if page > 0 else 0, ipp),
                inputs=[page, ipp],
                outputs=[log_table],
            ).then(lambda page: page - 1, inputs=[page], outputs=[page])
            refresh_btn.click(
                lambda page, ipp: get_messages(page, ipp),
                inputs=[page, ipp],
                outputs=[log_table],
            )
    with gr.Tab("User managenent"):
        with gr.Column(variant="panel"):
            gr.Markdown("## User managenent")
            with gr.Row():
                user_name = gr.Textbox(label="user name")
                user_password = gr.Textbox(label="user password")
                adduser_btn = gr.Button("Add")
                deluser_btn = gr.Button("Delete")
                update_user_btn = gr.Button("Update")
            users_df = gr.Dataframe(pd.DataFrame(get_users()), col_count=2)
            # gr.List(get_users())
            adduser_btn.click(
                lambda user_name, password: add_user(user_name, password),
                inputs=[user_name, user_password],
            ).then(lambda: pd.DataFrame(get_users()), outputs=users_df)
            deluser_btn.click(
                lambda user_name: delete_user(user_name), inputs=[user_name]
            ).then(lambda: pd.DataFrame(get_users()), outputs=users_df)
            update_user_btn.click(
                lambda user_name, password: update_user(user_name, password),
                inputs=[user_name, user_password],
            ).then(lambda: pd.DataFrame(get_users()), outputs=users_df)

    demo.load(update_messages, inputs=[page, ipp], outputs=[log_table])
    demo.load(lambda: gr.Dataframe(pd.DataFrame(get_users())), outputs=[users_df])

    demo.queue().launch(
        server_port=config["DASHBOARD_PORT"],
        auth=[(config["DASHBOARD_USER"], config["DASHBOARD_PASSWORD"])],
        root_path="/dash/",
    )
