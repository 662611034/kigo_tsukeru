'''
psd_toolsを用いて.psdファイルを操作するクラスを定義
'''
import psd_tools
import tkinter as tk
import tkinter.ttk as ttk

class PSDImageExt(psd_tools.PSDImage):
    '''
    PSDImageはpsdファイルを取り扱うクラスであり、それを継承して必要なメソッドを追加した

    Attributes
    ----------
    depth_max: int
        最大階層
    encoding: str
        ファイルの文字コード

    HEADSYMBOLS: tuple
        つけたり外したりする記号「!」と「*」のタプル

    Notes
    -----
    階層とはレイヤーが何重にグループに属しているかを表す数字であり、
    psdファイルそのものの階層を0、トップレイヤーの階層を1とし、グループに属すると1ずつ増える
    '''

    HEADSYMBOLS = ('!', '*')

    @classmethod
    def open(cls, filepath, encoding='sjis', **kwargs):
        '''
        もともとのopenメソッドをオーバーライドし、
        ファイルを開いた時の文字コードと最大階層を保存するようにする

        Parameters
        ----------
        filepath: str
            ファイルのパス
        encoding: str
            ファイルを開くときの文字コード
        '''
        psd = super(PSDImageExt, cls).open(filepath, encoding=encoding, **kwargs)
        psd.depth_max = psd.find_depth_max()
        psd.encoding = encoding
        return psd

    def find_depth_max(self):
        '''
        最大階層を調べるメソッド
        all_layersを実行し、階層の最大値を調べる

        Returns
        -------
        depth_max: int
        '''
        depth_max = 0
        for _, depth in self.all_layers():
            if depth > depth_max:
                depth_max = depth
        return depth_max

    def save(self, file_path, encoding=None, **kwargs):
        '''
        psdを保存するメソッド。親クラスのopenをオーバーライドする
        親クラスは文字コードを保存する機能がなく、指定がなければ既定のmacromanで実行される

        Parameters
        ----------
        encoding: str
            保存するとき使う文字コード。指定がなければopenの時保存したものが使われる
        '''
        if encoding is None:
            encoding = self.encoding
        super().save(file_path, encoding=encoding, **kwargs)
        return self

    @classmethod
    def sublayers_recursive(cls, layer, depth=0):
        '''
        引数として受け取ったレイヤーの下位レイヤーを深さ優先探索(合ってるよね？)で調べるジェネレータ
        layerクラスにはdepthという属性がないため、手動で与える必要がある
        
        Parameters
        ----------
        layer: psd_tools.api.layers.Group / PixelLayer
            レイヤーのインスタンス
        depth: int
            layerの階層

        Retunrs
        -------
        sublayer, subsublayer: psd_tools.api.layers.Group / PixelLayer
            下位レイヤー
        subdepth, subsubdepth: int
            その階層

        Notes
        -----
        今のところ階層はall_layersメソッドで何かするときぐらいしか使っていない
        いらない場合は適当な値を入れても特に問題ない
        '''
        if layer.is_group():
            for sublayer in layer:
                subdepth = depth + 1
                yield sublayer, subdepth
                for subsublayer, subsubdepth in cls.sublayers_recursive(sublayer, subdepth):
                    yield subsublayer, subsubdepth
    
    def all_layers(self):
        '''
        psdファイルのすべてのレイヤー、グループを調べるジェネレータ

        Returns
        -------
        layer: psd_tools.api.layers.Group / PixelLayer
            psdファイルに属するレイヤーやグループ
        depth: int
            階層

        Notes
        -----
        psd自身(階層0のオブジェクト)は除く
        psdファイル自身は特にいじる理由がないのと、
        ほかのレイヤーやグループとは属性が異なるから取り扱いが色々とややこしいため
        '''
        for layer, depth in self.sublayers_recursive(self):
            yield layer, depth

    def export_layers(self):
        '''
        psdファイルに属するすべてのレイヤーとグループ構造を文字列に変換して出力
        階層数に比例したインデント、枝分かれ記号、[レイヤー名]の形になる

        Returns
        -------
        content: str
            レイヤー構造を表した文字列
        '''
        content = ''
        for layer, depth in self.all_layers():
            content += str(depth) + ' ' * 2 * depth
            if depth > 1:
                content += '|-  '
            content += '[' + layer.name + ']\n'
        return content

    def layer_fullpath(self, layer, path=''):
        '''
        .anmファイル書き出しのためにレイヤーのフルパスを再帰的に調べるメソッド
        フルパスとは、どのグループに含まれているかを全て記したパスのこと
        親グループがPSDImageExt型になるまで調べ、それがpsdファイル自身でなければ例外を起こす

        Parameters
        ----------
        layer: psd_tools.api.layers.Group / PixelLayer
            フルパスを調べたいレイヤーやグループ
        path: str
            1個下位レイヤーのパス
            再帰的にパスを調べるために存在するものであり、メソッドを使うときは何も入力しない

        Returns
        -------
        fullpath: str
            レイヤーのフルパス
        '''
        if type(layer._parent) is type(self) and not (layer._parent is self):
            raise Exception('The layer is not a part of the psd')

        fullpath = layer.name + path
        if layer._parent is self:
            return fullpath
        else:
            return self.layer_fullpath(layer._parent, '/' + fullpath)

    def export_anmscript(self, layer, tracknum=0):
        '''
        .anmスクリプトを生成するメソッド
        psdtoolkitで「同じ階層のレイヤー全てをコピー」したときできる文字列のようなもの
        ただし、複数のグループで.anmファイルを生成するときに備えて、「--track~」部分と「local values~」部分を
        別々で返す

        Parameters
        ----------
        layer: psd_tools.api.layers.Group / PixelLayer
            スライダー化したいレイヤーがまとめられているグループ
            layerがグループでなければメソッドは改行のみを返す
        tracknum: int
            .anmで0, 1, 2, 3とつく番号

        Returns
        -------
        trackline: str
            「--trackなんたら」の文字列
        valueline: str
            「local values なんたら」から「PSD:addstateかんたら」のところまでの文字列
        '''
        if not layer.is_group():
            return '\n', '\n'

        trackline = f'--track{tracknum}:{layer.name},0,{len(layer)},0,1\n'
        valueline = 'local values = {\n'
        for sublayer in layer:
            fullpath = self.layer_fullpath(sublayer).replace(' ', '%20')
            valueline += f'  "v1.{fullpath}",\n'
        valueline += '}\n'
        valueline += f'PSD:addstate(values, obj.track{tracknum})\n'

        return trackline, valueline


if __name__ == '__main__':
    ifile = r'./sample.psd'
    psd0 = PSDImageExt.open(ifile, encoding='sjis')
    print(type(psd0[0][0][0]))
