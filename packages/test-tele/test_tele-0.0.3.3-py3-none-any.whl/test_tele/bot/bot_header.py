import logging
import shlex
import re
import os
from typing import Optional, Dict, Union

from test_tele.config_bot import BOT_CONFIG, write_bot_config


async def get_link_text(text: str) -> Optional[Union[str, Dict]]:
    pattern = r'(https:\/\/\S+\.\S+)'
    match = re.search(pattern, text)

    if not match:
        return None, None
    
    url = match.group(0)
    options = await get_options(text)

    return url, options


async def get_options(text: str) -> Dict:
    brand = await get_only_brand(text)
    args: list[str] = []
    options: Dict = {}

    r_val = re.search(r'-r\s+(\d+)', text)
    if r_val:
        options['r'] = int(r_val.group(1))
    o_val = re.search(r'-o\s+(\d+)', text)
    if o_val:
        options['o'] = int(o_val.group(1))

    if brand == 'twitter' or brand == 'x':
        if re.search(r'\+timeline', text):
            args.append('timeline')
        if re.search(r'\+media', text):
            args.append('media')
    elif brand == 'instagram':
        if re.search(r'\+highlight', text):
            args.append('highlight')

    options['args'] = args

    return options


async def get_only_brand(url: str) -> str:
    pattern = r"https?:\/\/(www.)?(\w+)\.\w+"
    match = re.search(pattern, url)
    return match.group(2)


async def get_user_config(user_id: str) -> Union[bool, int]:
    for i, item in enumerate(BOT_CONFIG.user_cfg):
        if item.user_id == user_id:
            return True, i
    return False, None
        

async def get_user_setting(recipient: str, **kwargs):
    check, i = await get_user_config(recipient)
    user = BOT_CONFIG.user_cfg
    link = f"{kwargs['url']}"

    command = []
    try:
        if check:
            ignore_config = "--config-ignore" if user[i].config_ignore else ""
            config_path = f"-c '{user[i].user_config_path}'" if user[i].config_ignore else ""

            count = user[i].count
            offset = user[i].offset
            
            if 'r' in kwargs['opt']:
                count = kwargs['opt']['r']
            if 'o' in kwargs['opt']:
                offset = kwargs['opt']['o']

            BOT_CONFIG.user_cfg[i].status = 1
            write_bot_config(BOT_CONFIG)

            if kwargs['opt']['args']:
                for item in kwargs['opt']['args']:
                    link = f"{kwargs['url']}/{item}"
                    cmd = shlex.split(f'gallery-dl {link} --range {offset + 1}-{count} -j {ignore_config} {config_path}')
                    command.append(cmd)
            else:
                cmd = shlex.split(f'gallery-dl {link} --range {offset + 1}-{count} -j {ignore_config} {config_path}')
                command.append(cmd)
        else:
            cmd = shlex.split(f'gallery-dl {link} --range 1-10 -j --config-ignore -c config/config.json')
            command.append(cmd)

        return command
    except Exception as e:
        logging.error(str(e))




    
















async def get_path_name(cmd_output):
    output = cmd_output[2:].replace('\\', '/')
    return os.path.split(output)




async def get_count_album(item):
    category = item[1] if await check_json(item[0], 2) else None
    link = item[1] if await check_json(item[0], 3) else None
    link_list = item[1] if await check_json(item[0], 6) else None
    
    return category, link, link_list


async def check_json(item, no) -> bool:
    return bool(item == no)


async def get_back_to_default(user_id):
    i = await get_user_config(user_id)
    try:
        BOT_CONFIG.user_cfg[i].offset = 0
        BOT_CONFIG.user_cfg[i].links = []
        BOT_CONFIG.user_cfg[i].status = 0

        write_bot_config(BOT_CONFIG)
    except:
        pass


async def check_status(user_id):
    i = await get_user_config(user_id)
    user = BOT_CONFIG.user_cfg

    if i and user[i].status == 1:
        return True
    return False