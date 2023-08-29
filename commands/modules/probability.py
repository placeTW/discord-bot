import random


def mock_bernoulli(p: float) -> bool:
    """Returns True with probability p.

    Args:
        p (float): a float between 0 and 1.

    Returns:
        bool: True or False.
    """
    return random.random() < p
