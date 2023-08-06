NAME
ģ������
========
::

    console_tool

DESCRIPTION
���
====
::

    �ṩ���������г��򹤾ߵ�ģ��,����Console�ࡣ
    A module for creating command line programs.

�������� CLASSES
''''''''''''''''
��̳�˳��::

    builtins.object::
        ColoredTextWrapper
        Console
    colorama.ansi.AnsiCursor(builtins.object)::
        Cursor

class Console
""""""""""""""""""""""""""""""
    bell(self, times=1, delay=False)::

        ��������������ն�,������������
        times:�������
        delay:��ʼ������Ƿ���������,Ĭ��ΪFalse��
    
    clear(self)
        ��������д����е������ı�, �⽫����ϵͳ��cls��clear���
    
    color(self, backcolor='', forecolor='')::

        �ı������д��ڵ�ǰ���ͱ�����ɫ
        ��coloredtext������ͬ,color�ı��������ڵ���ɫ
        �÷�������ϵͳ��color����
        ��::

           color("blue","green") -- ����ǰ����ɫΪ��ɫ,������ɫΪ��ɫ
           color() -- �ָ�Ĭ����ɫ

        ���õ���ɫ: black, blue, green, aqua, red, purple, yellow, white, gray, light_blue, light_green, light_aqua, light_red, light_purple, light_yellow, bright_white

    coloredtext(self, string, color='white', highlight=None, \*args, end='\n', flush=False, reset=True)::

        ���һ�δ���ɫ���ı�
        ��:coloredtext("Hello world!",color="green",highlight="black","bold") --
        �����ɫ���Ӵֵ�����'Hello world!'
        ����: ctext

    colorize(self, stdout='blue', stderr='red', bold=True)::

        ��ʼ������ɫ�����,������IDLE��
        colorize(stdout="cyan",stderr="magenta") - ���������ϢΪ��ɫ,������ϢΪ��ɫ��
        colorize(stderr=None) - ֻ���������Ϣ(sys.stdout)����ɫ��

    input(self, prompt='', chars_to_read=None, \*\*kwargs)::

        ��ȡ�û������롣
        prompt:��ʾ(Ĭ����ʾΪ��ɫ)
        chars_to_read:Ҫ��sys.stdin��ȡ���ٸ��ַ�

    print_slowly(self, iterable_of_str, delay=0, \*args, \*\*kwargs)::

        �����ش�ӡ��һ���ı�
        iterable_of_str:����ӡ������(�ַ�����ɵ�������)

    reset(self)::

        ��colorize�����෴,ֹͣ����ɫ�������

    title(self, title)::

        ���������д��ڱ��⡣

    ��������:

    resize(self, cols, lines)::

        ���Ŵ��ڡ�cols: ����, lines: ����

    chcp(self, codepage)::

        �ı�����ҳ, ʹ��chcp����


class Cursor
""""""""""""""""""""""""""""""""""""""
    Cursor(outfile=sys.stdout)
    
    �������еĹ����
    
    down(self, distance=1)
        �����ƶ����,����Ϊdistance��
    
    left(self, distance=1)
        �����ƶ����,����Ϊdistance��
    
    pos(self, x=1, y=1)
        �ƶ������ָ��λ��(x,y)��
        ������ṩ����x,y,���ƶ��������Ļ���Ͻǡ�
    
    right(self, distance=1)
        �����ƶ����,����Ϊdistance��
    
    up(self, distance=1)
        �����ƶ����,����Ϊdistance��

class ColoredTextWrapper(builtins.object)
    ColoredTextWrapper(file=sys.stdout, color='white', bold=True)

    ���������ṩ����ɫ�������,������IDLE
    
    flush(self)
    
    write(self, string)

ʾ������ EXAMPLES
=================
.. code-block:: python

    c=Console() #��ʼ��Console����
    c.colorize() 
    c.title("console_tool.py (Test)")
    c.coloredtext("Hello world!","green","magenta","blink") # �����ɫ��Hello world!

�汾 VERSION
============
    1.2.2

���� AUTHOR
===========
    *�߷ֳ��� qq:3076711200 �ٶ��˺�:�쵤34  ����:3416445406@qq.com*