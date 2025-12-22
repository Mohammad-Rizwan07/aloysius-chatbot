def detect_change(url, lastmod, new_hash, old_state):
    if url not in old_state:
        return "NEW"

    if old_state[url]["lastmod"] != lastmod:
        if old_state[url]["hash"] != new_hash:
            return "UPDATED"
        else:
            return "METADATA_ONLY"

    return "UNCHANGED"
