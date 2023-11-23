
def test_typical_flow():
    import branch_assigner.branch_assigner

    branch_assigner.branch_assigner.branch_env_dict = {
        "feature/do-mon-work": {"env_num": 1, "dev_name": "d01", "time_stamp": "05/15/2023 11AM"},
        "feature/do-wed-work": {"env_num": 2, "dev_name": "d02", "time_stamp": "05/17/2023 11AM"},
        "feature/do-fri-work": {"env_num": 3, "dev_name": "d03", "time_stamp": "05/19/2023 11AM"}
    }

    new_branch_info = branch_assigner.branch_assigner.create_branch("feature/do-sat-work")
    assert new_branch_info["env_num"] == 4
    assert new_branch_info["dev_name"] == "d04"
    assert len(branch_assigner.branch_assigner.branch_env_dict) == 4

    new_branch_info = branch_assigner.branch_assigner.create_branch("feature/do-wed-work")
    assert new_branch_info["env_num"] == 2
    assert new_branch_info["dev_name"] == "d02"

    branch_assigner.branch_assigner.delete_branch("feature/do-wed-work")
    assert len(branch_assigner.branch_assigner.branch_env_dict) == 3

    new_branch_info = branch_assigner.branch_assigner.create_branch("feature/do-FIVE-work")
    assert new_branch_info["env_num"] == 5
    assert new_branch_info["dev_name"] == "d05"
    assert len(branch_assigner.branch_assigner.branch_env_dict) == 4

    branch_info = branch_assigner.branch_assigner.get_branch_info("feature/do-mon-work")
    assert branch_info["env_num"] == 1
    assert branch_info["dev_name"] == "d01"
    assert len(branch_assigner.branch_assigner.branch_env_dict) == 4

    branch_info = branch_assigner.branch_assigner.get_branch_info("feature/NON-EXISTENT")
    assert branch_info["env_num"] == 0
    assert branch_info["dev_name"] == ""
    assert len(branch_assigner.branch_assigner.branch_env_dict) == 4


def test_when_list_is_empty():
    import branch_assigner.branch_assigner

    branch_assigner.branch_assigner.branch_env_dict = {
    }
    assert len(branch_assigner.branch_assigner.branch_env_dict) == 0

    new_branch_info = branch_assigner.branch_assigner.create_branch("feature/do-sat-work")
    assert new_branch_info["env_num"] == 1
    assert new_branch_info["dev_name"] == "d01"
    assert len(branch_assigner.branch_assigner.branch_env_dict) == 1