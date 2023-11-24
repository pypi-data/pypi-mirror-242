import nan_dev


def dice(ctx, message):
    return hasattr(message, "dice") and message.dice


nan_dev.filters.dice = dice
