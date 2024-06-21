from typing import Dict, Union
from tmll.tsp.services.tsp_service import TSPService
from tmll.tsp.utils.pattern_extractor import PatternExtractor

AVAILABLE_TREE_TYPES = ["xy", "timegraph", "data"]


class TreeService(TSPService):

    def get_tree(self, uuid: str, output_id: str, tree_type: str) -> Union[Dict[str, str], Dict[str, Dict[str, int]]]:
        """Get the tree for the given experiment UUID and output type.

        Args:
            uuid (str): The UUID which the tree belongs to.
            output_id (str): The output ID which the tree belongs to.
            tree_type (str): The type of tree to get. You can use get_tree_types() to get the available tree types.

        Returns:
            Union[Dict[str, str], Dict[str, Dict[str, int]]]: The tree for the given UUID and output type.
        """

        # Get the tree for the given experiment UUID and output type
        if tree_type == "xy":
            return self.__get_tree_xy(uuid, output_id)
        elif tree_type == "timegraph":
            return self.__get_tree_timegraph(uuid, output_id)
        elif tree_type == "data":
            return self.__get_tree(uuid, output_id)
        else:
            return {"error": "Invalid tree type."}

    @staticmethod
    def get_tree_types() -> list[str]:
        """Get the available tree types.

        Returns:
            list[str]: The available tree types.
        """
        return AVAILABLE_TREE_TYPES

    def __get_tree_xy(self, uuid: str, output_id: str) -> Union[Dict[str, str], Dict[str, Dict[str, int]]]:
        # Get the XY tree for the given experiment UUID and output type
        return self.__get_tree(uuid, output_id)

    def __get_tree_timegraph(self, uuid: str, output_id: str) -> Union[Dict[str, str], Dict[str, Dict[str, int]]]:
        # Get the timegraph tree for the given experiment UUID and output type
        return {"error": "Timegraph tree not implemented here yet."}

    def __get_tree(self, uuid: str, output_id: str) -> Union[Dict[str, str], Dict[str, Dict[str, int]]]:
        # Get the data tree for the given experiment UUID and output type
        command = ["python3", self.tsp_client_name, "--get-tree", output_id, "--uuid", uuid]
        execution = self.run_tsp_command(command)
        if "error" in execution:
            return execution

        process_output = execution["output"]
        tree = PatternExtractor.extract_tree(process_output)
        return tree
