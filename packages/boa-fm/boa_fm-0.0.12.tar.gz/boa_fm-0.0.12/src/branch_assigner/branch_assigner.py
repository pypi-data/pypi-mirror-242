branch_env_dict = {}


def create_branch(new_branch_name):
    # first, lets check if a branch by that name already exists. if so just use it
    dev_name = branch_env_dict.get(new_branch_name, None)
    if dev_name is not None:
        return dev_name

    # get all branches and see the highest number assigned so far
    # if no branch exists (empty dict) use 1
    max_env_number = max([bi["env_num"] for bi in branch_env_dict.values()], default=0) + 1

    new_branch_info = {
        "env_num": max_env_number,
        "dev_name": f'd{max_env_number:02d}',
        "time_stamp": "05/19/2023 11AM"
    }
    branch_env_dict[new_branch_name] = new_branch_info
    return new_branch_info


def delete_branch(branch_name):
    branch_env_dict.pop(branch_name)


def get_branch_info(branch_name):
    try:
        return branch_env_dict[branch_name]
    except KeyError:
        return {"env_num": 0, "dev_name": ""}
