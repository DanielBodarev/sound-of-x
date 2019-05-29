from sinestring import SineFull
from audio_utils import play_sine, save_sine
from expr_utils import Expr
from sampler import sample_fn

fn = SineFull(frequency="440", amplitude="0.25")

save_sine(fn)

