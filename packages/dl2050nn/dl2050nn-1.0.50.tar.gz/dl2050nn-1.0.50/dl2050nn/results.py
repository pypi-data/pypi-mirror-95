import numpy as np
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import matplotlib as mpl
from IPython.display import display
import sklearn
from dl2050nn.etc import *
from dl2050nn.data import TabularDataset
# https://en.wikipedia.org/wiki/Sensitivity_and_specificity

epsilon = 1e-9
scols = ['p','n','tp','fp','tn','fn','tpr','fpr','tnr','fnr','accuracy','error_rate','precision','recall',
         'sensitivity','specificity']

def df_stats_by_class(cm):
    rows = []
    for i in range(cm.shape[0]):
        precision = cm[i,i]/cm[i,:].sum()
        recall = cm[i,i]/(cm[:,i].sum()+epsilon)
        f1 = 2*(precision*recall)/(precision+recall+epsilon)
        support = cm[:,i].sum()
        rows.append((precision, recall, f1, support))
    return pd.DataFrame(rows, columns=['precision', 'recall', 'f1', 'support'])

def get_stats(preds, actuals, th=.5):
    p = np.sum(actuals==1)
    n = np.sum(actuals==0)
    tp = np.sum((preds==1)*(actuals==1)*1)
    fp = np.sum((preds==1)*(actuals==0)*1)
    tn = np.sum((preds==0)*(actuals==0)*1)
    fn = np.sum((preds==0)*(actuals==1)*1)
    tpr = tp/(p+epsilon)
    fpr = fp/(n+epsilon)
    tnr = tn/(n+epsilon)
    fnr = fn/(p+epsilon)
    accuracy = np.sum(preds==actuals)/(len(actuals))
    error_rate = 1.-accuracy
    precision = tp/(tp+fp+epsilon)
    recall = tpr
    sensitivity = recall
    specificity = tnr
    return [p,n,tp,fp,tn,fn,tpr,fpr,tnr,fnr,accuracy,error_rate,precision,recall,sensitivity,specificity], scols

def df_stats_binary(preds, actuals, th=.5):
    stats, stats_cols = get_stats(preds, actuals, th=.5)
    stats = [len(actuals)]+stats
    cols = ['total']+stats_cols
    return pd.DataFrame([stats], columns=cols)

def df_stats_cum(probs, actuals, th=.5, thresholds=None):
    mask = np.argsort(-probs)
    actuals, probs = actuals[mask], probs[mask]
    preds = (probs>=th)*1
    ptotal = np.sum(actuals==1)
    nn = np.arange(len(actuals))+1
    nnp = nn/len(actuals)
    p = np.cumsum(actuals==1)
    n = np.cumsum(actuals==0)
    tp = np.cumsum((preds==1)*(actuals==1)*1)
    fp = np.cumsum((preds==1)*(actuals==0)*1)
    tn = np.cumsum((preds==0)*(actuals==0)*1)
    fn = np.cumsum((preds==0)*(actuals==1)*1)
    tpr = tp / (p+epsilon)
    fpr = fp / (n+epsilon)
    tnr = tn / (n+epsilon)
    fnr = fn / (p+epsilon)
    accuracy = np.cumsum(preds==actuals)/(nn)
    error_rate = 1.-accuracy
    precision = tp/(tp+fp+epsilon)
    recall = tpr
    sensitivity = recall
    specificity = tnr
    pcaptured = tp/ptotal
    z = zip(probs,preds,actuals,nn,nnp,p,n,tp,fp,tn,fn,tpr,fpr,tnr,fnr,accuracy,error_rate,precision,recall,sensitivity,specificity,pcaptured)
    cols = ['prob','pred','actual','size','size%']+scols+['pcaptured']
    df = pd.DataFrame(z, columns=cols)
    if thresholds:
        ths = [t/thresholds if t>0 else -.00001 for t in range(0,thresholds)[::-1]]
        ths2, idxs = [], []
        for t in ths:
            idxs1 = np.where(probs>t)[0]
            if len(idxs1):
                ths2.append(t)
                idxs.append(max(idxs1))
        df = df.iloc[idxs].copy()
        df.insert(0, 'threshold', ths2)
        df.drop(columns=['prob','pred','actual'], inplace=True)
    return df

def plot_cmap(data):
    fig, ax = plt.subplots(figsize=(8, 8))
    cmap=sns.diverging_palette(0, 160, as_cmap=True)
    cmap=mpl.cm.Blues
    cmap = sns.diverging_palette(0, 180, sep=40, s=100, as_cmap=True)
    sns.heatmap(data, vmin=-1, vmax=1, cmap=cmap, square=True, ax=ax)
    plt.show()
    plt.pause(.001)

def plot_confusion(c, actuals, preds):
    cm = np.zeros((c, c), dtype=int)
    cm_p = np.zeros((c, c), dtype=np.float)
    for i in range(preds.shape[0]): cm[int(actuals[i])][int(preds[i])] += 1
    for i in range(cm.shape[0]): cm_p[i,:] = cm[i,:] / cm[i,:].sum()
    cm_p = 100.0*cm_p
    fig = plt.figure(figsize=(20, 5))
    ax1, ax2 = fig.add_subplot(121), fig.add_subplot(122)
    sns.set(font_scale=1.0)
    sns.heatmap(cm, cmap=mpl.cm.Blues, annot=True, fmt='d', ax=ax1)
    sns.heatmap(cm_p, cmap=mpl.cm.Blues, annot=True, fmt='.2f', ax=ax2)
    ax1.set_title(f'Total: {preds.shape[0]}')
    ax2.set_title(f'Total: 100.00%')
    plt.show()
    plt.pause(.001)
    return cm

def calc_prc(y, y2):
    mask = np.argsort(-y2)
    y, y2 = y[mask], y2[mask]
    recall = np.array([0]+[((y2>=t)[y==1]==y[y==1]).sum()/(y==1).sum() for t in y2]+[1])
    precision = np.array([1]+[(y[y2>=t]==1).sum()/(y2>=t).sum() for t in y2]+[0])
    auc_pr = np.trapz(precision, recall)
    return auc_pr, precision, recall

def calc_roc(y, y2):
    mask = np.argsort(-y2)
    y, y2 = y[mask], y2[mask]
    fpr = np.array([0]+[((y2>=t)[y==0]!=y[y==0]).sum()/(y==0).sum() for t in y2])
    tpr = np.array([0]+[((y2>=t)[y==1]==y[y==1]).sum()/(y==1).sum() for t in y2])
    auc = np.trapz(tpr, fpr)
    return auc, fpr, tpr

# def np_resample_with_mean(x,k): return np.mean(x[:k*(len(x)//k)].reshape(-1, k), 1)

def plot_roc(y, y2):
    fpr,tpr,_ = sklearn.metrics.roc_curve(y, y2)
    auc = auc = np.trapz(tpr, fpr)
    precision,recall,_ = sklearn.metrics.precision_recall_curve(y, y2)
    auc_pr = np.trapz(precision, recall)
    # auc, fpr, tpr = calc_roc(y, y2)
    # auc_pr, precision, recall = calc_prc(y, y2)
    _, axs = plt.subplots(1,2, figsize=(14,5))
    axs[0].plot(fpr, tpr, label=f'AUC = {auc:.3f})')
    axs[0].plot([0., 1.], [0., 1.], 'k--')
    axs[0].set_title('ROC')
    axs[0].set_xlabel('FPR')
    axs[0].set_ylabel('TPR = Recall')
    axs[0].legend(loc='best')
    cut = len(recall) - int(len(recall)/100)
    axs[1].plot(recall[:cut], precision[:cut], label=f'AUC_PR = {auc_pr:.3f})')
    axs[1].plot([0., 1.], [1., 0.], 'k--')
    axs[1].set_title('ROC - Precision/Recall')
    axs[1].set_xlabel('Recall')
    axs[1].set_ylabel('Precision')
    axs[1].legend(loc='best')
    plt.show()
    plt.pause(.001)

def get_corr(df, cols, c=None, plot=False, max_vars=None):
    dfc = df[cols].corr()
    if c is not None:
        dfc=dfc[c].copy()
        n = max_vars or len(dfc)
        dfc = pd.DataFrame(dfc.reindex(dfc.abs().sort_values(ascending=False).index)[:n])
        dfc = dfc.drop(index=[c])
    display(dfc)
    if plot: plot_cmap(dfc)

def get_probs(y2): return np.exp(np.max(y2, axis=1))
def get_probs_bin(y2): return np.exp(y2[:,1])
def get_preds(probs, t=.5): return (probs>t)*1

def get_predictions_clsf(model, x, device='cpu'):
    model.eval()
    with torch.no_grad():
        x = x.to(device)
        y2 = model(x)
    return y2.detach().cpu().numpy()
# x = torch.cat([x for x,y in learner.data.dl2])

def get_predictions_clsf_tabular(data, model, df, device='cpu'):
    dfp = data.proc(df.copy())
    x = dfp[data.proc.c2].values
    x = torch.from_numpy(x).float()
    y2 = get_predictions_clsf(model, x, device)
    prob = get_probs(y2) if data.c>2 else get_probs_bin(y2)
    pred = get_preds(prob)
    df['prob'] = prob
    df['pred'] = pred
    df['pred_label'] = [data.cls[e] for e in pred]
    return df


# ???
def get_probs_for_actuals(y2, actuals):
    probs = np.exp(y2)
    mask = np.zeros((probs.shape[0], probs.shape[1]))
    mask[np.arange(actuals.shape[0]),actuals] = 1
    return probs[mask.astype(bool)]


# ???
def df_predict_clsf(learner, df, have_actuals=False):
    df = df.copy()
    if 'prob' in df.columns: df=df.drop(columns='prob')
    data = learner.data
    y2 = learner.predict(df)
    y2 = y2.numpy()
    prob = get_probs(y2) if data.c>2 else get_probs_bin(y2)
    pred = get_preds(y2)
    pred_label = [data.cls[e] for e in pred]
    df['prob'] = prob
    df['pred'] = pred
    df['pred_label'] = pred_label
    if have_actuals:
        actuals = df[data.proc.c_dep] 
        df['actual'] = actuals.values
        df['actual_label'] = [data.cls[e] for e in actuals.values]
        df['error'] = (df['pred']!=df['actual'])*1
    df = df.sort_values(by=['prob'], ascending=[False])
    return df


class Results_Clsf():
    def __init__(self, probs, actuals):
        self.probs, self.actuals = probs, actuals
        self.preds = get_preds(probs)
        self.c = len(np.unique(actuals))
#         self.probs_for_actuals = get_probs_for_actuals(y2, self.actuals)
#         self.probs_sorted = np.argsort(self.probs_for_actuals)[::-1]
    def show_all(self, thresholds=10):
        self.confusion()
        self.roc()
        display(self.df_stats(thresholds=thresholds))
    def confusion(self, t=None):
        show_dist(self.actuals)
        display(df_stats_binary(self.preds, self.actuals))
        if t is None:
            preds = self.preds
        else:
            if self.c!=2: raise ValueError('More than two classes')
            preds = (self.probs>t)*1
        cm = plot_confusion(self.c, self.actuals, preds)
        display(df_stats_by_class(cm))
    def df_stats(self, thresholds=10):
        if self.c!=2: raise ValueError('More than two classes')
        return df_stats_cum(self.probs, self.actuals, thresholds=thresholds)
    def roc(self):
        if self.c!=2: raise ValueError('More than two classes')
        plot_roc(self.actuals, self.probs)
#     def show_best(self, n=8, **kwargs):  self.show_set(self.data.ds2, self.probs_sorted[:n], **kwargs)
#     def show_worst(self, n=8, **kwargs): self.show_set(self.data.ds2, self.probs_sorted[-n:][::-1], **kwargs)
#     def show_set(self, ds, idxs, **kwargs):
#         labels = [f'{ds.labels[i]}:{self.actuals[i]} -> {ds.cls[self.preds[i]]}:{self.preds[i]} (p={self.probs_for_actuals[i]:.4f})'
#                     for i in idxs]
#         ds.show(list(idxs), labels=labels, **kwargs)


class Results_Clsf_Tabular(Results_Clsf):
    def __init__(self, data, df):
        assert 'prob' in df.columns
        assert data.proc.c_dep in df.columns
        self.proc, self.df = data.proc, df
        super(Results_Clsf_Tabular, self).__init__(df['prob'].values, df[data.proc.c_dep].values)
        # self.df['prob'] = self.probs if self.data.c>2 else self.probs_bin
    # def corr_cat(self): get_corr(self.df, self.proc.c_cat, plot=True)
    # def corr_cont(self): get_corr(self.df, self.proc.c_cont, plot=True)
    # def corr_prob(self): get_corr(self.df, self.proc.c_cat+self.proc.c_cont+[self.proc.c_dep, 'prob'], c='prob', plot=True)
