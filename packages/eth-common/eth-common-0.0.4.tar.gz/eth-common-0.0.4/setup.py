import setuptools

setuptools.setup(
    include_package_data=True,
    version=open('eth_common/resources/version').read(),
    #cmdclass=versioneer.get_cmdclass()
)