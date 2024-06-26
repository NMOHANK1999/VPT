import os
import argparse
import torch
import torchvision

from videogpt import VideoData, VideoGPT, load_videogpt
from videogpt.utils import save_video_grid
import ipdb


parser = argparse.ArgumentParser()
parser.add_argument('--ckpt', type=str, default='bair_gpt')
parser.add_argument('--n', type=int, default=1)
args = parser.parse_args()
n = args.n

if not os.path.exists(args.ckpt):
    gpt = load_videogpt(args.ckpt)
else:
    gpt = VideoGPT.load_from_checkpoint(args.ckpt)
gpt = gpt.cuda()
gpt.eval()
args = gpt.hparams['args']

args.batch_size = n
# data = VideoData(args)
# loader = data.test_dataloader()
# batch = next(iter(loader))
# batch = {k: v.cuda() for k, v in batch.items()}
frame_fname = '0.png'
frame = torchvision.io.read_image(frame_fname)
trans = torchvision.transforms.ConvertImageDtype(torch.float32)
frame = trans(frame)


samples = gpt.sample_frame(n, frame)
ipdb.set_trace()
save_video_grid(samples, 'samples.mp4')
