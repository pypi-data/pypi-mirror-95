import time
import numpy as np
import pytest

from sklearn.datasets import fetch_20newsgroups
from dirty_cat import GapEncoder

@pytest.mark.parametrize("hashing, init, analyzer, add_words", [
    (False, 'k-means++', 'word', True),
    (True, 'random', 'char', False),
    (True, 'k-means', 'char_wb', True)
])
def test_gap_encoder(hashing, init, analyzer, add_words, n_samples=70):
    X_txt = fetch_20newsgroups(subset='train')['data']
    X = X_txt[:n_samples]
    n_components = 10
    # Test output shape
    encoder = GapEncoder(
        n_components=n_components, hashing=hashing, init=init,
        analyzer=analyzer, add_words=add_words,
        random_state=42, rescale_W=True)
    encoder.fit(X)
    y = encoder.transform(X)
    assert y.shape == (n_samples, n_components), str(y.shape)
    assert len(set(y[0])) == n_components

    # Test L1-norm of topics W.
    l1_norm_W = np.abs(encoder.W_).sum(axis=1)
    np.testing.assert_array_almost_equal(
        l1_norm_W, np.ones(n_components))

    # Test same seed return the same output
    encoder = GapEncoder(
        n_components=n_components, hashing=hashing, init=init,
        analyzer=analyzer, add_words=add_words,
        random_state=42)
    encoder.fit(X)
    y2 = encoder.transform(X)
    np.testing.assert_array_equal(y, y2)
    return


def test_input_type():
    # Numpy array
    X = np.array(['alice', 'bob'])
    enc = GapEncoder(n_components=2, random_state=42)
    X_enc_array = enc.fit_transform(X)
    # List
    X = ['alice', 'bob']
    enc = GapEncoder(n_components=2, random_state=42)
    X_enc_list = enc.fit_transform(X)
    # Check if the encoded vectors are the same
    np.testing.assert_array_equal(X_enc_array, X_enc_list)
    return


def test_partial_fit(n_samples=70):
    X_txt = fetch_20newsgroups(subset='train')['data']
    X = X_txt[:n_samples]
    # Gap encoder with fit on one batch
    enc = GapEncoder(random_state=42, batch_size=n_samples, max_iter=1)
    X_enc = enc.fit_transform(X)
    # Gap encoder with partial fit
    enc = GapEncoder(random_state=42)
    enc.partial_fit(X)
    X_enc_partial = enc.transform(X)
    # Check if the encoded vectors are the same
    np.testing.assert_array_equal(X_enc, X_enc_partial)
    return


def test_get_feature_names(n_samples=70):
    X_txt = fetch_20newsgroups(subset='train')['data']
    X = X_txt[:n_samples]
    enc = GapEncoder()
    enc.fit(X)
    topic_labels = enc.get_feature_names()
    # Check number of labels
    assert len(topic_labels) == enc.n_components
    return
    

def profile_encoder(Encoder, init):
    # not an unit test
    
    from dirty_cat import datasets
    employee_salaries = datasets.fetch_employee_salaries()
    data = employee_salaries['data']
    X = data['employee_position_title'].tolist()
    t0 = time.time()
    encoder = Encoder(n_components=50, init=init)
    encoder.fit(X)
    y = encoder.transform(X)
    assert y.shape == (len(X), 50)
    eta = time.time() - t0
    return eta


if __name__ == '__main__':
    print('start test_gap_encoder')
    test_gap_encoder(True, 'k-means++', 'char', False)
    print('test_gap_encoder passed')
    print('start test_input_type')
    test_input_type()
    print('test_input_type passed')
    print('start test_partial_fit')
    test_partial_fit()
    print('test_partial_fit passed')
    print('start test_get_feature_names')
    test_get_feature_names()
    print('test_get_feature_names passed')
    
    for _ in range(3):
        print('time profile_encoder(GapEncoder, init="k-means++")')
        print("{:.4} seconds".format(profile_encoder(
            GapEncoder, init='k-means++')))
    for _ in range(3):
        print('time profile_encoder(GapEncoder, init="k-means")')
        print("{:.4} seconds".format(profile_encoder(
            GapEncoder, init='k-means')))
    
    print('Done')
