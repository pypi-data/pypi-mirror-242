from typing import Any, Dict, List, Type, TypeVar, cast

import attr

from ..models.product_stream_brew_tags import ProductStreamBrewTags
from ..models.product_stream_channels_item import ProductStreamChannelsItem
from ..models.product_stream_composes import ProductStreamComposes
from ..models.product_stream_product_variants_item import (
    ProductStreamProductVariantsItem,
)
from ..models.product_stream_product_versions_item import (
    ProductStreamProductVersionsItem,
)
from ..models.product_stream_products_item import ProductStreamProductsItem
from ..models.product_stream_relations_item import ProductStreamRelationsItem
from ..models.tag import Tag
from ..types import UNSET, ComponentRegistryModel, Unset

T = TypeVar("T", bound="ProductStream")


@attr.s(auto_attribs=True)
class ProductStream(ComponentRegistryModel):
    """Show detailed information for ProductStream(s).
    Add or remove fields using ?include_fields=&exclude_fields="""

    link: str
    uuid: str
    ofuri: str
    name: str
    description: str
    build_count: int
    builds: str
    components: str
    upstreams: str
    tags: List[Tag]
    channels: List[ProductStreamChannelsItem]
    active: bool
    brew_tags: ProductStreamBrewTags
    cpes: List[str]
    cpes_matching_patterns: List[str]
    yum_repositories: List[str]
    composes: ProductStreamComposes
    et_product_versions: List[str]
    exclude_components: List[str]
    manifest: str
    relations: List[ProductStreamRelationsItem]
    products: List[ProductStreamProductsItem]
    product_versions: List[ProductStreamProductVersionsItem]
    product_variants: List[ProductStreamProductVariantsItem]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        link = self.link
        uuid = self.uuid
        ofuri = self.ofuri
        name = self.name
        description = self.description
        build_count = self.build_count
        builds = self.builds
        components = self.components
        upstreams = self.upstreams
        tags: List[Dict[str, Any]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = []
            for tags_item_data in self.tags:
                tags_item: Dict[str, Any] = UNSET
                if not isinstance(tags_item_data, Unset):
                    tags_item = tags_item_data.to_dict()

                tags.append(tags_item)

        channels: List[Dict[str, Any]] = UNSET
        if not isinstance(self.channels, Unset):
            channels = []
            for channels_item_data in self.channels:
                channels_item: Dict[str, Any] = UNSET
                if not isinstance(channels_item_data, Unset):
                    channels_item = channels_item_data.to_dict()

                channels.append(channels_item)

        active = self.active
        brew_tags: Dict[str, Any] = UNSET
        if not isinstance(self.brew_tags, Unset):
            brew_tags = self.brew_tags.to_dict()

        cpes: List[str] = UNSET
        if not isinstance(self.cpes, Unset):
            cpes = self.cpes

        cpes_matching_patterns: List[str] = UNSET
        if not isinstance(self.cpes_matching_patterns, Unset):
            cpes_matching_patterns = self.cpes_matching_patterns

        yum_repositories: List[str] = UNSET
        if not isinstance(self.yum_repositories, Unset):
            yum_repositories = self.yum_repositories

        composes: Dict[str, Any] = UNSET
        if not isinstance(self.composes, Unset):
            composes = self.composes.to_dict()

        et_product_versions: List[str] = UNSET
        if not isinstance(self.et_product_versions, Unset):
            et_product_versions = self.et_product_versions

        exclude_components: List[str] = UNSET
        if not isinstance(self.exclude_components, Unset):
            exclude_components = self.exclude_components

        manifest = self.manifest
        relations: List[Dict[str, Any]] = UNSET
        if not isinstance(self.relations, Unset):
            relations = []
            for relations_item_data in self.relations:
                relations_item: Dict[str, Any] = UNSET
                if not isinstance(relations_item_data, Unset):
                    relations_item = relations_item_data.to_dict()

                relations.append(relations_item)

        products: List[Dict[str, Any]] = UNSET
        if not isinstance(self.products, Unset):
            products = []
            for products_item_data in self.products:
                products_item: Dict[str, Any] = UNSET
                if not isinstance(products_item_data, Unset):
                    products_item = products_item_data.to_dict()

                products.append(products_item)

        product_versions: List[Dict[str, Any]] = UNSET
        if not isinstance(self.product_versions, Unset):
            product_versions = []
            for product_versions_item_data in self.product_versions:
                product_versions_item: Dict[str, Any] = UNSET
                if not isinstance(product_versions_item_data, Unset):
                    product_versions_item = product_versions_item_data.to_dict()

                product_versions.append(product_versions_item)

        product_variants: List[Dict[str, Any]] = UNSET
        if not isinstance(self.product_variants, Unset):
            product_variants = []
            for product_variants_item_data in self.product_variants:
                product_variants_item: Dict[str, Any] = UNSET
                if not isinstance(product_variants_item_data, Unset):
                    product_variants_item = product_variants_item_data.to_dict()

                product_variants.append(product_variants_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        if not isinstance(link, Unset):
            field_dict["link"] = link
        if not isinstance(uuid, Unset):
            field_dict["uuid"] = uuid
        if not isinstance(ofuri, Unset):
            field_dict["ofuri"] = ofuri
        if not isinstance(name, Unset):
            field_dict["name"] = name
        if not isinstance(description, Unset):
            field_dict["description"] = description
        if not isinstance(build_count, Unset):
            field_dict["build_count"] = build_count
        if not isinstance(builds, Unset):
            field_dict["builds"] = builds
        if not isinstance(components, Unset):
            field_dict["components"] = components
        if not isinstance(upstreams, Unset):
            field_dict["upstreams"] = upstreams
        if not isinstance(tags, Unset):
            field_dict["tags"] = tags
        if not isinstance(channels, Unset):
            field_dict["channels"] = channels
        if not isinstance(active, Unset):
            field_dict["active"] = active
        if not isinstance(brew_tags, Unset):
            field_dict["brew_tags"] = brew_tags
        if not isinstance(cpes, Unset):
            field_dict["cpes"] = cpes
        if not isinstance(cpes_matching_patterns, Unset):
            field_dict["cpes_matching_patterns"] = cpes_matching_patterns
        if not isinstance(yum_repositories, Unset):
            field_dict["yum_repositories"] = yum_repositories
        if not isinstance(composes, Unset):
            field_dict["composes"] = composes
        if not isinstance(et_product_versions, Unset):
            field_dict["et_product_versions"] = et_product_versions
        if not isinstance(exclude_components, Unset):
            field_dict["exclude_components"] = exclude_components
        if not isinstance(manifest, Unset):
            field_dict["manifest"] = manifest
        if not isinstance(relations, Unset):
            field_dict["relations"] = relations
        if not isinstance(products, Unset):
            field_dict["products"] = products
        if not isinstance(product_versions, Unset):
            field_dict["product_versions"] = product_versions
        if not isinstance(product_variants, Unset):
            field_dict["product_variants"] = product_variants

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy() if isinstance(src_dict, dict) else {}
        link = d.pop("link", UNSET)

        uuid = d.pop("uuid", UNSET)

        ofuri = d.pop("ofuri", UNSET)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        build_count = d.pop("build_count", UNSET)

        builds = d.pop("builds", UNSET)

        components = d.pop("components", UNSET)

        upstreams = d.pop("upstreams", UNSET)

        tags = []
        _tags = d.pop("tags", UNSET)
        if _tags is UNSET:
            tags = UNSET
        else:
            for tags_item_data in _tags or []:
                _tags_item = tags_item_data
                tags_item: Tag
                if isinstance(_tags_item, Unset):
                    tags_item = UNSET
                else:
                    tags_item = Tag.from_dict(_tags_item)

                tags.append(tags_item)

        channels = []
        _channels = d.pop("channels", UNSET)
        if _channels is UNSET:
            channels = UNSET
        else:
            for channels_item_data in _channels or []:
                _channels_item = channels_item_data
                channels_item: ProductStreamChannelsItem
                if isinstance(_channels_item, Unset):
                    channels_item = UNSET
                else:
                    channels_item = ProductStreamChannelsItem.from_dict(_channels_item)

                channels.append(channels_item)

        active = d.pop("active", UNSET)

        _brew_tags = d.pop("brew_tags", UNSET)
        brew_tags: ProductStreamBrewTags
        if isinstance(_brew_tags, Unset):
            brew_tags = UNSET
        else:
            brew_tags = ProductStreamBrewTags.from_dict(_brew_tags)

        cpes = cast(List[str], d.pop("cpes", UNSET))

        cpes_matching_patterns = cast(List[str], d.pop("cpes_matching_patterns", UNSET))

        yum_repositories = cast(List[str], d.pop("yum_repositories", UNSET))

        _composes = d.pop("composes", UNSET)
        composes: ProductStreamComposes
        if isinstance(_composes, Unset):
            composes = UNSET
        else:
            composes = ProductStreamComposes.from_dict(_composes)

        et_product_versions = cast(List[str], d.pop("et_product_versions", UNSET))

        exclude_components = cast(List[str], d.pop("exclude_components", UNSET))

        manifest = d.pop("manifest", UNSET)

        relations = []
        _relations = d.pop("relations", UNSET)
        if _relations is UNSET:
            relations = UNSET
        else:
            for relations_item_data in _relations or []:
                _relations_item = relations_item_data
                relations_item: ProductStreamRelationsItem
                if isinstance(_relations_item, Unset):
                    relations_item = UNSET
                else:
                    relations_item = ProductStreamRelationsItem.from_dict(
                        _relations_item
                    )

                relations.append(relations_item)

        products = []
        _products = d.pop("products", UNSET)
        if _products is UNSET:
            products = UNSET
        else:
            for products_item_data in _products or []:
                _products_item = products_item_data
                products_item: ProductStreamProductsItem
                if isinstance(_products_item, Unset):
                    products_item = UNSET
                else:
                    products_item = ProductStreamProductsItem.from_dict(_products_item)

                products.append(products_item)

        product_versions = []
        _product_versions = d.pop("product_versions", UNSET)
        if _product_versions is UNSET:
            product_versions = UNSET
        else:
            for product_versions_item_data in _product_versions or []:
                _product_versions_item = product_versions_item_data
                product_versions_item: ProductStreamProductVersionsItem
                if isinstance(_product_versions_item, Unset):
                    product_versions_item = UNSET
                else:
                    product_versions_item = ProductStreamProductVersionsItem.from_dict(
                        _product_versions_item
                    )

                product_versions.append(product_versions_item)

        product_variants = []
        _product_variants = d.pop("product_variants", UNSET)
        if _product_variants is UNSET:
            product_variants = UNSET
        else:
            for product_variants_item_data in _product_variants or []:
                _product_variants_item = product_variants_item_data
                product_variants_item: ProductStreamProductVariantsItem
                if isinstance(_product_variants_item, Unset):
                    product_variants_item = UNSET
                else:
                    product_variants_item = ProductStreamProductVariantsItem.from_dict(
                        _product_variants_item
                    )

                product_variants.append(product_variants_item)

        product_stream = cls(
            link=link,
            uuid=uuid,
            ofuri=ofuri,
            name=name,
            description=description,
            build_count=build_count,
            builds=builds,
            components=components,
            upstreams=upstreams,
            tags=tags,
            channels=channels,
            active=active,
            brew_tags=brew_tags,
            cpes=cpes,
            cpes_matching_patterns=cpes_matching_patterns,
            yum_repositories=yum_repositories,
            composes=composes,
            et_product_versions=et_product_versions,
            exclude_components=exclude_components,
            manifest=manifest,
            relations=relations,
            products=products,
            product_versions=product_versions,
            product_variants=product_variants,
        )

        product_stream.additional_properties = d
        return product_stream

    @staticmethod
    def get_fields():
        return {
            "link": str,
            "uuid": str,
            "ofuri": str,
            "name": str,
            "description": str,
            "build_count": int,
            "builds": str,
            "components": str,
            "upstreams": str,
            "tags": List[Tag],
            "channels": List[ProductStreamChannelsItem],
            "active": bool,
            "brew_tags": ProductStreamBrewTags,
            "cpes": List[str],
            "cpes_matching_patterns": List[str],
            "yum_repositories": List[str],
            "composes": ProductStreamComposes,
            "et_product_versions": List[str],
            "exclude_components": List[str],
            "manifest": str,
            "relations": List[ProductStreamRelationsItem],
            "products": List[ProductStreamProductsItem],
            "product_versions": List[ProductStreamProductVersionsItem],
            "product_variants": List[ProductStreamProductVariantsItem],
        }

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
