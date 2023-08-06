from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(["AnnotatedTree/Layer/*.pyx",
                           "AnnotatedTree/*.pyx",
                           "AnnotatedTree/Processor/Condition/*.pyx",
                           "AnnotatedTree/Processor/*.pyx",
                           "AnnotatedTree/Processor/NodeModification/*.pyx",
                           "AnnotatedTree/Processor/LeafConverter/*.pyx",
                           "AnnotatedTree/Processor/LayerExist/*.pyx"],
                          compiler_directives={'language_level': "3"}),
    name='NlpToolkit-AnnotatedTree-Cy',
    version='1.0.7',
    packages=['AnnotatedTree', 'AnnotatedTree.Layer', 'AnnotatedTree.Processor', 'AnnotatedTree.Processor.Condition',
              'AnnotatedTree.Processor.LayerExist', 'AnnotatedTree.Processor.LeafConverter',
              'AnnotatedTree.Processor.NodeModification'],
    package_data={'AnnotatedTree': ['*.pxd', '*.pyx', '*.c', '*.py'],
                  'AnnotatedTree.Layer': ['*.pxd', '*.pyx', '*.c', '*.py'],
                  'AnnotatedTree.Processor': ['*.pxd', '*.pyx', '*.c', '*.py'],
                  'AnnotatedTree.Processor.Condition': ['*.pxd', '*.pyx', '*.c', '*.py'],
                  'AnnotatedTree.Processor.LayerExist': ['*.pxd', '*.pyx', '*.c', '*.py'],
                  'AnnotatedTree.Processor.LeafConverter': ['*.pxd', '*.pyx', '*.c', '*.py'],
                  'AnnotatedTree.Processor.NodeModification': ['*.pxd', '*.pyx', '*.c', '*.py']},
    url='https://github.com/StarlangSoftware/AnnotatedTree-Cy',
    license='',
    author='olcaytaner',
    author_email='olcay.yildiz@ozyegin.edu.tr',
    description='Annotated constituency treebank library',
    install_requires = ['NlpToolkit-AnnotatedSentence-Cy', 'NlpToolkit-ParseTree-Cy', 'NlpToolkit-FrameNet-Cy']
)
