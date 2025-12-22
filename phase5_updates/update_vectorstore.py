def delete_vectors_by_url(collection, url):
    collection.delete(where={"url": url})
