# import pytest
# import numpy as np
# from nautilus_nlp.utils.file_loader import documents_loader, list_files, detect_encoding


# testdoc_latin1 = "J'aime les frites bien grasse étalon châpeau!"
# encoded_s = testdoc_latin1.encode('latin-1')

# with open('testfolder_fileloader/testdoc_latin1.txt', 'wb') as f:
#     f.write(encoded_s)

# testdoc_utf8 = "Un deuxième exemple de texte en utf-8 cette fois!"
# encoded_s = testdoc_utf8.encode('utf-8')
# with open('./testfolder_fileloader/testdoc_utf8.txt', 'wb') as f:
#     f.write(encoded_s)

# def test_openfile_with_encoding():
#     input_str = "testfolder_fileloader/testdoc_latin1.txt"
#     expected_str = testdoc_latin1

#     result = documents_loader(input_str, encoding='latin-1')
#     np.testing.assert_string_equal(result, expected_str)

# def test_openfile_utf8():
#     input_str = "testfolder_fileloader/testdoc_utf8.txt"
#     expected_str = testdoc_utf8

#     result = documents_loader(input_str)
#     np.testing.assert_string_equal(result, expected_str)

# def test_encoding_detection():
#     input_str = "testfolder_fileloader/testdoc_latin1.txt"
#     expected_str = testdoc_latin1

#     result = documents_loader(input_str)
#     np.testing.assert_string_equal(result, expected_str)    
    
# def test_load_several_docs_wildcard():
#     expected = {'testfolder_fileloader/testdoc_latin1.txt': "J'aime les frites bien grasse étalon châpeau!",
#                 'testfolder_fileloader/testdoc_utf8.txt': 'Un deuxième exemple de texte en utf-8 cette fois!'}
#     result = documents_loader('testfolder_fileloader/*.txt', output_as='dict')
#     np.testing.assert_equal(result, expected)    

# def test_load_several_docs_list():
#     expected = {'testfolder_fileloader/testdoc_latin1.txt': "J'aime les frites bien grasse étalon châpeau!",
#                 'testfolder_fileloader/testdoc_utf8.txt': 'Un deuxième exemple de texte en utf-8 cette fois!'}
#     result = documents_loader(['testfolder_fileloader/testdoc_latin1.txt','testfolder_fileloader/testdoc_utf8.txt'], output_as='dict')
#     np.testing.assert_equal(result, expected)


# def test_load_several_docs_output_list():
#     expected = ["J'aime les frites bien grasse étalon châpeau!",
#                 'Un deuxième exemple de texte en utf-8 cette fois!']
#     result = documents_loader(['testfolder_fileloader/testdoc_latin1.txt','testfolder_fileloader/testdoc_utf8.txt'], output_as='list')
#     return len(expected) == len(result) and sorted(expected) == sorted(result)



# @pytest.mark.parametrize("input_filepath", ['testfolder_fileloader/*.txt','testfolder_fileloader/','testfolder_fileloader'])
# def test_list_files(input_filepath):
#     expected = ['testfolder_fileloader/testdoc_latin1.txt','testfolder_fileloader/testdoc_utf8.txt']
#     result = list_files(input_filepath)

#     return len(expected) == len(result) and sorted(expected) == sorted(result)


# def test_detect_encoding():
#     expected = {'encoding': 'ISO-8859-1', 'confidence': 0.73, 'language': ''}
#     result = detect_encoding('testfolder_fileloader/testdoc_latin1.txt')

#     np.testing.assert_equal(result, expected)

