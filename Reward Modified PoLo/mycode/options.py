import argparse
import numpy as np
    
def read_options():
    parser = argparse.ArgumentParser()

    parser.add_argument('--input_dir', default='datasets/Hetionet/', type=str)

    parser.add_argument('--base_output_dir', default='output/Hetionet/', type=str)

    parser.add_argument('--rule_file', default='rules.txt', type=str)

    parser.add_argument('--pretrained_embeddings_dir', default='', type=str)

    parser.add_argument('--load_model', default=0, type=int)

    parser.add_argument('--model_load_path', default='models/Hetionet/', type=str)

    parser.add_argument('--total_iterations', default=1000, type=int) #1000, minimum must be 10, as folder creation every 10 iterations, else model saving wont find saving path

    parser.add_argument('--eval_every', default=10, type=int)

    parser.add_argument('--patience', default=3, type=int)

    parser.add_argument('--seed', default=42, type=int, nargs='+')

    parser.add_argument('--batch_size', default=128, type=int, nargs='+')

    parser.add_argument('--num_rollouts', default=30, type=int, nargs='+')

    parser.add_argument('--test_rollouts', default=100, type=int, nargs='+')

    parser.add_argument('--path_length', default=3, type=int, nargs='+')

    parser.add_argument('--max_num_actions', default=400, type=int, nargs='+') #400, cannot be 40

    parser.add_argument('--hidden_size', default=64, type=int, nargs='+')

    parser.add_argument('--embedding_size', default=64, type=int, nargs='+')

    parser.add_argument('--LSTM_layers', default=2, type=int, nargs='+')

    parser.add_argument('--learning_rate', default=6e-4, type=float, nargs='+') #6e-4

    parser.add_argument('--beta', default=0.05, type=float, nargs='+')

    parser.add_argument('--gamma', default=1, type=float, nargs='+')

    parser.add_argument('--Lambda', default=0.02, type=float, nargs='+')

    parser.add_argument('--grad_clip_norm', default=5, type=int, nargs='+')

    parser.add_argument('--rule_base_reward', default=1, type=float, nargs='+')
        
    parser.add_argument('--positive_reward', default=1.0, type=float, nargs='+')

    parser.add_argument('--negative_reward', default=0, type=float, nargs='+')

    parser.add_argument('--only_body', default=0, type=int, nargs='+')

    parser.add_argument('--pool', default='max', type=str)

    parser.add_argument('--use_entity_embeddings', default=1, type=int)

    parser.add_argument('--train_entity_embeddings', default=1, type=int)

    parser.add_argument('--train_relation_embeddings', default=1, type=int)
    
    parser.add_argument('--theta1', default=0.28, type=float, nargs='+')
    
    parser.add_argument('--theta2',  default=31.22, type=float, nargs='+')

    parser.add_argument('--alpha', default=0.25, type=float, nargs='+')

    try:
        parsed = vars(parser.parse_args())
    except IOError as msg:
        parser.error(str(msg))

    parsed['use_entity_embeddings'] = (parsed['use_entity_embeddings'] == 1)
    parsed['train_entity_embeddings'] = (parsed['train_entity_embeddings'] == 1)
    parsed['train_relation_embeddings'] = (parsed['train_relation_embeddings'] == 1)

    if parsed['pretrained_embeddings_dir'] != '':
        parsed['pretrained_embeddings_relation'] = parsed['pretrained_embeddings_dir'] + 'relation_embeddings.npy'
        parsed['pretrained_embeddings_entity'] = parsed['pretrained_embeddings_dir'] + 'entity_embeddings.npy'
        parsed['pretrained_relation_to_id'] = parsed['pretrained_embeddings_dir'] + 'relation_to_id.json'
        parsed['pretrained_entity_to_id'] = parsed['pretrained_embeddings_dir'] + 'entity_to_id.json'
    else:
        parsed['pretrained_embeddings_relation'] = ''
        parsed['pretrained_embeddings_entity'] = ''

    maxLen = max([len(k) for k in parsed.keys()])
    fmtString = '\t%' + str(maxLen) + 's : %s'
    print('Arguments:')
    for keyPair in sorted(parsed.items()):
        print(fmtString % keyPair)
    return parsed

