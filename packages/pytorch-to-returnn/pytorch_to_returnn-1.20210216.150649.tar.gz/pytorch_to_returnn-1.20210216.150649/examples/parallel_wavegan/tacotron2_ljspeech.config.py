#!rnn.py

config = globals()["config"]  # make IDEs happy

# mode selection
MODE = config.value("mode", "train")
assert MODE in ['train', 'gta_decoding']

# global settings
debug_mode = False
debug_print_layer_output_shape=False
debug_print_layer_output_template=True
device = 'gpu'
log = ['./returnn.log']
log_batch_size = True
log_verbosity = 5
# model = 'returnn_models/window_epoch_t2'
model = 'returnn_models/window_epoch'

# choose eval_task if we run GTA decoding
if MODE=='gta_decoding':
    task='eval'
else:
    task = 'train'

# tensorflow settings
tf_log_memory_usage = True

# learning rate and gradient control
accum_grad_multiple_step = 2
gradient_clip = 1
gradient_noise = 0
learning_rate_control = 'newbob_multi_epoch'
learning_rate_control_min_num_epochs_per_new_lr = 5
learning_rate_control_relative_error_relative_lr = True
learning_rate_file = 'returnn_training_lr_scores'
learning_rates = [0.001]
use_learning_rate_control_always = True

# newbob learning rate control
newbob_learning_rate_decay = 0.9
newbob_multi_num_epochs = 5
newbob_multi_update_interval = 1
newbob_relative_error_threshold = 0

# gradient optimizer
optimizer = {'class': 'adam', 'epsilon': 1e-08}

# data feeding
batch_size = 28000
extern_data = {
    'classes': {'dim': 77, 'shape': (None,), 'sparse': True, 'available_for_inference': True},
    'data': {'dim': 80, 'shape': (None, 80), 'available_for_inference': False},
}
max_seq_length = {'data': 1000}
max_seqs = 200

#training
cleanup_old_models = True
num_epochs = 200
save_interval = 1
stop_on_nonfinite_train_score = False

# dataset defintion
def get_dataset(type):
    global_parameters = { 
        'class': 'OggZipDataset',
        'audio': { 
            'feature_options': {'fmin': 60, 'fmax': 7600},
            'features': 'db_mel_filterbank',
            'join_frames': 1,
            'norm_mean': -74.8469952583313,
            'norm_std_dev': 32.351323967712815,
            'num_feature_filters': 80,
            'peak_normalization': False,
            'preemphasis': 0.97,
            'step_len': 0.0125,
            'window_len': 0.05},
        'targets': {
            'class': 'Vocabulary',
            'unknown_label': None,
            'vocab_file': 'data/cmu_vocab.pkl'},
        'path': 'data/LJSpeech.ogg.zip',
        'partition_epoch': 1,
    }
    if type == "dev":
        dev_parameters = {
            'segment_file': 'data/dev_segments.txt',
            'seq_ordering': 'sorted',
        }
        dataset_parameters = {**global_parameters, **dev_parameters}
    if type == "train":
        train_parameters = {
            'segment_file': 'data/train_segments.txt',
            'seq_ordering': 'laplace:.1000',
        }
        dataset_parameters = {**global_parameters, **train_parameters}
    return dataset_parameters

if MODE=='gta_decoding':
    dev = get_dataset("train")
    train = None
else:
    dev = get_dataset("dev")
    train = get_dataset("train")

# Network template
network_template = { 
    'decoder': { 'cheating': False,
        'class': 'rec',
        'from': [],
        'max_seq_len': 1000,
        'target': 'windowed_data_target',
        'unit': { 
            'accum_att_weights': {'class': 'combine',
                                  'kind': 'add',
                                  'from': ['prev:accum_att_weights', 'att_weights'],
                                  'is_output_layer': True},
            'att0': {'base': 'base:encoder', 'class': 'generic_attention', 'weights': 'att_weights'},
            'att_energy': {'activation': None, 'class': 'linear', 'from': ['att_energy_tanh'], 'n_out': 1, 'with_bias': False},
            'att_energy_in': { 'class': 'combine',
                               'from': ['base:enc_ctx', 's_transformed', 'location_feedback_transformed'],
                               'kind': 'add',
                               'n_out': 128},
            'att_energy_tanh': {'activation': 'tanh', 'class': 'activation', 'from': ['att_energy_in']},
            'att_weights': {'class': 'softmax_over_spatial', 'from': ['att_energy']},
            'choice': {'beam_size': 1, 'class': 'choice', 'from': ['output'],
                       'input_type': 'regression', 'target': 'windowed_data_target',
                       'n_out': 160},
            'convolved_att': { 'L2': 1e-07,
                               'activation': None,
                               'class': 'conv',
                               'filter_size': (31,),
                               'from': ['feedback_pad_right'],
                               'n_out': 32,
                               'padding': 'valid'},
            'decoder_1': { 'class': 'rnn_cell',
                           'from': ['pre_net_layer_2_out', 'prev:att0'],
                           'n_out': 640,
                           'unit': 'zoneoutlstm',
                           'unit_opts': {'zoneout_factor_cell': 0.1, 'zoneout_factor_output': 0.1}},
            'decoder_2': { 'class': 'rnn_cell',
                           'from': ['decoder_1'],
                           'n_out': 640,
                           'unit': 'zoneoutlstm',
                           'unit_opts': {'zoneout_factor_cell': 0.1, 'zoneout_factor_output': 0.1}},
            'end_compare': {'class': 'compare', 'from': ['stop_token_sigmoid'], 'kind': 'greater', 'value': 0.5},
            'end': {'class': 'squeeze', 'from': ['end_compare'], 'axis': 'F'},
            'entropy': { 'class': 'eval',
                         'eval': '-tf.reduce_sum(source(0)*safe_log(source(0)), axis=-1, keepdims=True)',
                         'from': ['att_weights'],
                         'loss': 'as_is',
                         'loss_scale': 0.0001},
            'feedback_pad_left': { 'axes': 's:0',
                                   'class': 'pad',
                                   'from': ['prev:accum_att_weights'],
                                   'mode': 'constant',
                                   'padding': ((15, 0),),
                                   'value': 1},
            'feedback_pad_right': { 'axes': 's:0',
                                    'class': 'pad',
                                    'from': ['feedback_pad_left'],
                                    'mode': 'constant',
                                    'padding': ((0, 15),),
                                    'value': 0},
            'location_feedback_transformed': { 'L2': 1e-07,
                                               'activation': None,
                                               'class': 'linear',
                                               'dropout': 0.1,
                                               'from': ['convolved_att'],
                                               'n_out': 128,
                                               'with_bias': False},
            'output': { 'activation': None,
                        'class': 'linear',
                        'from': ['decoder_2', 'att0'],
                        'loss': 'mean_l1',
                        'loss_scale': 1.0,
                        'n_out': 160,
                        'target': 'windowed_data_target'},
            'pre_net_layer_1': {'L2': 1e-07, 'activation': 'relu', 'class': 'linear', 'from': ['pre_slice'], 'n_out': 128},
            'pre_net_layer_2': { 'L2': 1e-07,
                                 'activation': 'relu',
                                 'class': 'linear',
                                 'dropout': 0.5,
                                 'dropout_noise_shape': {'*': None},
                                 'dropout_on_forward': True,
                                 'from': ['pre_net_layer_1'],
                                 'n_out': 64},
            'pre_net_layer_2_out': { 'class': 'dropout',
                                     'dropout': 0.5,
                                     'dropout_noise_shape': {'*': None},
                                     'dropout_on_forward': True,
                                     'from': ['pre_net_layer_2']},
            'pre_slice': {'axis': 'F', 'class': 'slice', 'from': ['prev:choice'], 'slice_start': 80},
            's_transformed': { 'L2': 1e-07,
                               'activation': None,
                               'class': 'linear',
                               'dropout': 0.5,
                               'from': ['decoder_2'],
                               'n_out': 128,
                               'with_bias': False},
            'stop_token': { 'activation': None,
                            'class': 'linear',
                            'from': ['decoder_2', 'att0'],
                            'loss': 'bin_ce',
                            'loss_scale': 1.0,
                            'n_out': 1,
                            'target': 'stop_token_target'},
            'stop_token_sigmoid': {'activation': 'sigmoid', 'class': 'activation', 'from': ['stop_token']}}},
  'embed_batchnorm_cv_0': {'class': 'batch_norm', 'from': ['embed_conv0']},
  'embed_batchnorm_cv_1': {'class': 'batch_norm', 'from': ['embed_conv1']},
  'embed_batchnorm_cv_2': {'class': 'batch_norm', 'from': ['embed_conv2']},
  'embed_conv0': {'L2': 1e-07, 'activation': 'relu', 'class': 'conv', 'filter_size': (5,), 'from': ['embedding'], 'n_out': 128, 'padding': 'same'},
  'embed_conv0_out': {'class': 'dropout', 'dropout': 0.5, 'dropout_noise_shape': {"*": None}, 'from': ['embed_batchnorm_cv_0']},
  'embed_conv1': { 'L2': 1e-07,
                   'activation': 'relu',
                   'class': 'conv',
                   'filter_size': (5,),
                   'from': ['embed_conv0_out'],
                   'n_out': 128,
                   'padding': 'same'},
  'embed_conv1_out': {'class': 'dropout', 'dropout': 0.5, 'dropout_noise_shape': {"*": None}, 'from': ['embed_batchnorm_cv_1']},
  'embed_conv2': { 'L2': 1e-07,
                   'activation': 'relu',
                   'class': 'conv',
                   'filter_size': (5,),
                   'from': ['embed_conv1_out'],
                   'n_out': 128,
                   'padding': 'same'},
  'embed_conv2_out': {'class': 'dropout', 'dropout': 0.5, 'dropout_noise_shape': {"*": None}, 'from': ['embed_batchnorm_cv_2']},
  'embedding': {'activation': None, 'class': 'linear', 'from': ['data:classes'], 'n_out': 128},
  'enc_ctx': { 'L2': 1e-07,
               'activation': None,
               'class': 'linear',
               'dropout': 0.5,
               'from': ['encoder', 'encoder_position'],
               'n_out': 128,
               'with_bias': True},
  'encoder': {'class': 'copy', 'dropout': 0.0, 'from': ['lstm0_fw', 'lstm0_bw']},
  'encoder_position': {'class': 'positional_encoding', 'from': ['lstm0_fw'], 'n_out': 64, 'out_type': {'dim': 64, 'shape': (None, 64)}},
  'lstm0_bw': { 'class': 'rec',
                'direction': -1,
                'from': ['embed_conv2_out'],
                'n_out': 256,
                'unit': 'zoneoutlstm',
                'unit_opts': {'zoneout_factor_cell': 0.1, 'zoneout_factor_output': 0.1}},
  'lstm0_fw': { 'class': 'rec',
                'direction': 1,
                'from': ['embed_conv2_out'],
                'n_out': 256,
                'unit': 'zoneoutlstm',
                'unit_opts': {'zoneout_factor_cell': 0.1, 'zoneout_factor_output': 0.1}},
  'mse_output': {'class': 'copy', 'from': ['output'], 'loss': 'mse', 'loss_scale': 0.0, 'n_out': 80, 'target': 'padded_data_target'},
  'output': { 'class': 'combine',
              'from': ['dec_output', 'post_conv_tf'],
              'kind': 'add',
              'loss': 'mean_l1',
              'loss_scale': 0.25,
              'n_out': 80,
              'target': 'padded_data_target'},
  'dec_output_split': {'class': 'split_dims',
                   'from': ['decoder'],
                   'axis': 'F',
                   'dims': (2, -1)},
  'dec_output': {'class': 'merge_dims',
                     'from': ['dec_output_split'],
                     'axes': ['T', 'static:0'],
                     'n_out': 80,},
  'post_batchnorm_cv_0': {'class': 'batch_norm', 'from': ['post_conv0']},
  'post_batchnorm_cv_1': {'class': 'batch_norm', 'from': ['post_conv1']},
  'post_batchnorm_cv_2': {'class': 'batch_norm', 'from': ['post_conv2']},
  'post_batchnorm_cv_3': {'class': 'batch_norm', 'from': ['post_conv3']},
  'post_batchnorm_cv_4': {'class': 'batch_norm', 'from': ['post_conv4']},
  'post_conv0': { 'L2': 1e-07,
                  'activation': 'relu',
                  'class': 'conv',
                  'filter_size': (5,),
                  'from': ['dec_output'],
                  'n_out': 256,
                  'padding': 'same'},
  'post_conv0_out': {'class': 'dropout', 'dropout': 0.5, 'dropout_noise_shape': {"*": None}, 'from': ['post_batchnorm_cv_0']},
  'post_conv1': { 'L2': 1e-07,
                  'activation': 'relu',
                  'class': 'conv',
                  'filter_size': (5,),
                  'from': ['post_conv0_out'],
                  'n_out': 256,
                  'padding': 'same'},
  'post_conv1_out': {'class': 'dropout', 'dropout': 0.5, 'dropout_noise_shape': {"*": None}, 'from': ['post_batchnorm_cv_1']},
  'post_conv2': { 'L2': 1e-07,
                  'activation': 'relu',
                  'class': 'conv',
                  'filter_size': (5,),
                  'from': ['post_conv1_out'],
                  'n_out': 256,
                  'padding': 'same'},
  'post_conv2_out': {'class': 'dropout', 'dropout': 0.5, 'dropout_noise_shape': {"*": None}, 'from': ['post_batchnorm_cv_2']},
  'post_conv3': { 'L2': 1e-07,
                  'activation': 'relu',
                  'class': 'conv',
                  'filter_size': (5,),
                  'from': ['post_conv2_out'],
                  'n_out': 256,
                  'padding': 'same'},
  'post_conv3_out': {'class': 'dropout', 'dropout': 0.5, 'dropout_noise_shape': {"*": None}, 'from': ['post_batchnorm_cv_3']},
  'post_conv4': { 'L2': 1e-07,
                  'activation': 'relu',
                  'class': 'conv',
                  'filter_size': (5,),
                  'from': ['post_conv3_out'],
                  'n_out': 256,
                  'padding': 'same'},
  'post_conv4_out': {'class': 'dropout', 'dropout': 0.5, 'dropout_noise_shape': {"*": None}, 'from': ['post_batchnorm_cv_4']},
  'post_conv_tf': {'activation': None, 'class': 'conv', 'filter_size': (5,), 'from': ['post_conv4_out'], 'n_out': 80, 'padding': 'same'},
  'stop_token_target': { 'class': 'eval',
                         'eval': "self.network.get_config().typed_value('_stop_token_target')(source(0, as_data=True))",
                         'from': ['windowed_data_target'],
                         'out_type': {'dim': 1, 'shape': (None, 1)},
                         'register_as_extern_data': 'stop_token_target'},
  'windowed_data': {'class': 'window',
                    'from': ['data'],
                    'window_size': 2,
                    'window_right': 1,
                    'stride': 2
                    },
  'padded_data_target': {'class': 'merge_dims',
                         'from': ['windowed_data'],
                         'axes': ['T', 'static:0'],
                         'n_out': 80,
                         'register_as_extern_data': 'padded_data_target',},
  'windowed_data_target': {'class': 'merge_dims',
                           'from': ['windowed_data'],
                           'axes': 'static',
                           'n_out': 160,
                           'register_as_extern_data': 'windowed_data_target',}
  }


if MODE=='gta_decoding':
    network_template['dump_output'] = {'class': 'hdf_dump', 'filename': 'data/gta_decode.hdf', 'from': 'output', 'is_output_layer': True}

# Dynamic network construction
def get_network(epoch, **kwargs):
    pretrain_stage = epoch // 5
    network = network_template
    if pretrain_stage < 5:
        postnet_loss_scale = max(min((pretrain_stage/5*0.25), 0.25), 0.01)
        stop_token_loss_scale = min(pretrain_stage/5, 1.0) 
        network['output']['loss_scale'] = postnet_loss_scale
        network['decoder']['unit']['stop_token']['loss_scale'] = stop_token_loss_scale 

    return network


def _stop_token_target(data, ramp_length=5):
  import tensorflow as tf
  time_axis = data.get_dynamic_axes()[0]
  stop_position = tf.expand_dims(data.get_dynamic_size(time_axis), axis=1) - ramp_length - 1
  ramp = tf.expand_dims(tf.range(tf.shape(data.placeholder)[1]), axis=0)
  full_ramp = tf.tile(ramp, [tf.shape(data.placeholder)[0], 1])
  adapted_ramp = tf.minimum(tf.maximum(full_ramp - stop_position, 0), ramp_length)
  return tf.cast(tf.expand_dims(adapted_ramp, 2), dtype="float32") / ramp_length

