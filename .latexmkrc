add_cus_dep('aux', 'glslog', 0, 'run_makeglossaries');
sub run_makeglossaries {
    system("makeglossaries -d build \"$_[0]\"");
}
