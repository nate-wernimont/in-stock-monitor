import boto3

client = boto3.client('sns')
response = client.publish(
    TopicArn="arn:aws:sns:us-east-1:432125680059:stock-update",
    Message="https://www.staples.com/evga-08g-p5-3663-kr-geforce-rtx-3060-ti-xc-gaming-hdmi-pci-express-4-0-x16-8gb-video/product_IM18PX706",
)
print(response)