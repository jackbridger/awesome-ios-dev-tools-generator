import openai
import os
from dotenv import load_dotenv
import json
load_dotenv()

INPUT_FILE_PATH = './data/tools.json'
openai.api_key = os.getenv("OPENAI_API_KEY")

EXAMPLE_BODY = "<div>The best universal clipboard manager for Mac, iPhone and iPad. Save, search and organize your pasteboard history by app, smart item type and collections</div><div><br></div><div>PastePal is a native application written in pure Swift that allows complete control over your clipboard history.</div><div><br></div><div>The app is universal and available across Mac, iPhone and iPad devices. You can manually enable iCloud Sync in Settings and all data will be securely synced across devices</div><div><br></div><div>Many features</div><ul><li>Light and dark mode</li><li>Side window for quick access to recent history. You can position it either top, left, bottom, right of the screen</li><li>Main window for complete overview. There you can filter by app, content type and organize into collections</li><li>Pagination. For large amount of data, pagination is enabled where you can navigate among multiple pages of history</li><li>Setup allow and ignored list of apps, folders, content words</li><li>Trim down pale history automatically. You can define time frame for how long you want to keep history</li><li>Keyboard shortcut to toggle windows, copy and delete history item</li><li>Accessible via status menu bar</li></ul>"

def summarize_body(description):
    prompt = generate_prompt(description)
    summary = send_prompt_to_open_ai(prompt)
    return summary

def generate_prompt(description):
    return """{}

    Summarise the above in 140 characters or less
    """.format(description)

def add_summary_to_tools():
    f = open(INPUT_FILE_PATH)
    data = json.load(f)
    print(type(data))
    list_of_categories_containing_tools = []
    for category in data:
        list_of_tools_in_this_category = []
        formatted_category = json.loads(category['json_agg'])
        for tool in formatted_category:
            summary = summarize_body(tool['long_body'])
            tool["summary_140_or_less"]= summary
            list_of_tools_in_this_category.append(tool)
        category['json_agg'] = list_of_tools_in_this_category
        formatted_category = json.dumps(category)
        list_of_categories_containing_tools.append(formatted_category)
    return list_of_categories_containing_tools

def dump_to_json(data_in_list):
    with open('data.json', 'w') as f:
        json.dump(data_in_list, f) 

def send_prompt_to_open_ai(prompt):
    response = openai.Completion.create(
        model="text-curie-001",
        prompt=prompt,
        temperature=0.7,
        max_tokens=64,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    summary = response['choices'][0]['text']
    return summary
