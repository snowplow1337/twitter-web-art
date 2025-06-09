import random
import time
from PIL import Image, ImageDraw
import tweepy
import requests

# Twitter API credentials (replace with your own)
consumer_key = 'your_twitter_consumer_key'
consumer_secret = 'your_twitter_consumer_secret'
access_token = 'your_twitter_access_token'
access_token_secret = 'your_twitter_access_token_secret'

# Pinata API credentials (replace with your own)
pinata_api_key = 'your_pinata_api_key'
pinata_secret_api_key = 'your_pinata_secret_api_key'

# Authenticate to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Generate abstract art
def generate_art(seed):
    random.seed(seed)
    img = Image.new('RGB', (500, 500), color='white')
    draw = ImageDraw.Draw(img)
    for _ in range(10):
        x = random.randint(0, 500)
        y = random.randint(0, 500)
        radius = random.randint(10, 50)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color)
    img.save('art.png')

# Get current timestamp as seed
seed = int(time.time())
generate_art(seed)

# Upload to Pinata (IPFS)
headers = {
    'pinata_api_key': pinata_api_key,
    'pinata_secret_api_key': pinata_secret_api_key,
}
files = {'file': open('art.png', 'rb')}
response = requests.post('https://api.pinata.cloud/pinning/pinFileToIPFS', headers=headers, files=files)
ipfs_hash = response.json()['IpfsHash']
ipfs_url = f'https://gateway.pinata.cloud/ipfs/{ipfs_hash}'

# Post to Twitter
status = f'Abstract art generated with code. View on IPFS: {ipfs_url}. DM me for web3 development services!'
api.update_status(status=status)
print('Tweet posted successfully!')